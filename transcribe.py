# transcribe.py — URL download + local transcription (faster-whisper)
from __future__ import annotations
import os, tempfile, subprocess, logging, shutil
from typing import Optional
from faster_whisper import WhisperModel
import numpy as np
try:
    import soundfile as sf  # type: ignore
except Exception:
    sf = None  # optional; if missing we will trust the uploaded WAV

logger = logging.getLogger("mymuse")

# ---- Env config ----
FFMPEG_BIN = os.getenv("FFMPEG_BIN", "ffmpeg")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")              # tiny/base/small/medium/large-v3
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")# "int8","float16","int8_float16",...
ENABLE_LINK_DOWNLOAD = os.getenv("ENABLE_LINK_DOWNLOAD", "true").lower() in ("1","true","yes","on")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# Default to openai if key is present; otherwise local
TRANSCRIBE_BACKEND = (os.getenv("TRANSCRIBE_BACKEND") or ("openai" if OPENAI_API_KEY else "local")).lower()

# ---- Utilities ----
def _discover_ffmpeg() -> Optional[str]:
    """Try to find ffmpeg if not on PATH or FFMPEG_BIN is wrong.
    Checks PATH, common Windows install paths (winget/choco/manual), and returns the first hit.
    """
    # 1) PATH
    p = shutil.which("ffmpeg")
    if p:
        return p
    # 2) Env-provided path that might be relative
    if FFMPEG_BIN and shutil.which(FFMPEG_BIN):
        return shutil.which(FFMPEG_BIN)
    # 3) Common Windows paths
    candidates = [
        r"C:\\Program Files\\FFmpeg\\bin\\ffmpeg.exe",
        r"C:\\Program Files\\Gyan\\FFmpeg\\bin\\ffmpeg.exe",
        r"C:\\ProgramData\\chocolatey\\bin\\ffmpeg.exe",
        r"C:\\ffmpeg\\bin\\ffmpeg.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    # 4) Bundled binary via imageio-ffmpeg (Python package)
    try:
        import imageio_ffmpeg  # type: ignore
        ipath = imageio_ffmpeg.get_ffmpeg_exe()
        if ipath and os.path.exists(ipath):
            return ipath
    except Exception:
        pass
    return None

def _ensure_ffmpeg() -> None:
    global FFMPEG_BIN
    try:
        subprocess.run([FFMPEG_BIN, "-version"], capture_output=True, check=True)
        return
    except Exception:
        alt = _discover_ffmpeg()
        if alt:
            FFMPEG_BIN = alt
            try:
                subprocess.run([FFMPEG_BIN, "-version"], capture_output=True, check=True)
                return
            except Exception:
                pass
        raise RuntimeError(
            "ffmpeg not found. Install FFmpeg and restart, or set FFMPEG_BIN to the full path (e.g., "
            "C:/Program Files/FFmpeg/bin/ffmpeg.exe)."
        )

def _normalize_wav_no_ffmpeg(src_path: str) -> Optional[str]:
    """Create a guaranteed PCM16, 16 kHz, mono WAV without using ffmpeg.
    Returns path to normalized temp file, or None if not possible.
    """
    if sf is None:
        return None
    try:
        data, sr = sf.read(src_path, always_2d=True)
        # Require 16kHz; we avoid resampling server-side to keep deps light
        if int(sr) != 16000:
            return None
        # Downmix to mono
        mono = data.mean(axis=1).astype(np.float32)
        dst = tempfile.mktemp(suffix=".wav")
        sf.write(dst, mono, 16000, subtype="PCM_16")
        return dst
    except Exception as e:
        logger.warning("WAV normalize failed: %s", e)
        return None

def _to_wav(src_path: str) -> str:
    """Ensure 16kHz mono wav.
    - For .wav: normalize to PCM16 mono (if possible) without ffmpeg.
    - For others: requires ffmpeg.
    """
    ext = os.path.splitext(src_path)[1].lower()
    if ext == ".wav":
        norm = _normalize_wav_no_ffmpeg(src_path)
        return norm or src_path
    _ensure_ffmpeg()
    dst = tempfile.mktemp(suffix=".wav")
    cmd = [FFMPEG_BIN, "-y", "-i", src_path, "-ac", "1", "-ar", "16000", "-f", "wav", dst]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return dst

# ---- Public: transcribe local file ----
def transcribe_media(file_path: str) -> str:
    """
    Transcribe local media (mp4/mp3/mov/webm/wav/etc.) to text.
    Backend: OpenAI Whisper (if TRANSCRIBE_BACKEND=openai and key present) else local faster-whisper.
    Returns transcript text; returns a dev-safe fallback on errors.
    """
    logger.info("Transcribe backend selected: %s", TRANSCRIBE_BACKEND)
    # Prefer OpenAI if requested and key is available
    if TRANSCRIBE_BACKEND == "openai" and OPENAI_API_KEY:
        try:
            import requests
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
            data = {"model": "whisper-1", "temperature": "0"}
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
                r = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, data=data, files=files, timeout=120)
            if r.status_code >= 400:
                logger.warning("OpenAI Whisper HTTP %s: %s", r.status_code, r.text[:300])
            else:
                j = r.json()
                txt = (j.get("text") or "").strip()
                if txt:
                    logger.info("Transcribed %s via openai/whisper-1 (REST)", os.path.basename(file_path))
                    return txt
                logger.warning("OpenAI Whisper returned empty text; falling back to local")
        except Exception as e:
            logger.warning("OpenAI Whisper REST failed, falling back to local: %s", e)

    # Local fallback: faster-whisper (no ffmpeg if you upload ready .wav)
    try:
        wav = _to_wav(file_path)
    except Exception as e:
        logger.warning("Transcode/normalize failed: %s", e)
        return "Sample transcript (dev fallback). Install ffmpeg + faster-whisper for real transcription."

    try:
        model = WhisperModel(WHISPER_MODEL, compute_type=WHISPER_COMPUTE_TYPE)
        segments, info = model.transcribe(wav, vad_filter=True)
        text = " ".join(s.text.strip() for s in segments if s.text).strip() or " "
        logger.info("Transcribed %s via local/%s", os.path.basename(file_path), WHISPER_MODEL)
        return text if text.strip() else "Sample transcript (dev fallback)."
    except Exception as e:
        logger.warning("Whisper error: %s", e)
        return "Sample transcript (dev fallback)."
    finally:
        try:
            os.remove(wav)
        except Exception:
            pass

# ---- URL download helpers ----
def _download_media(url: str) -> Optional[str]:
    """Download media from URL (Reels/TikTok/YT/etc.) using yt-dlp. Returns local path or None."""
    if not ENABLE_LINK_DOWNLOAD:
        logger.info("Link download disabled by env (ENABLE_LINK_DOWNLOAD=false)")
        return None
    try:
        import yt_dlp  # type: ignore
    except Exception:
        logger.warning("yt-dlp not installed; cannot download from URL")
        return None

    tempdir = tempfile.mkdtemp(prefix="muse_dl_")
    outtmpl = os.path.join(tempdir, "media.%(ext)s")
    ydl_opts = {"outtmpl": outtmpl, "quiet": True, "noplaylist": True, "nocheckcertificate": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info)
            logger.info("Downloaded URL to %s", path)
            return path
    except Exception as e:
        logger.warning("yt-dlp error: %s", e)
        try: shutil.rmtree(tempdir, ignore_errors=True)
        except Exception: pass
        return None

# One-shot helper: transcribe from URL
def transcribe_from_url(url: str) -> Optional[str]:
    path = _download_media(url)
    if not path:
        return None
    try:
        return transcribe_media(path)
    finally:
        try: os.remove(path)
        except Exception: pass

# Compatibility alias some apps expect
def download_from_url(url: str) -> Optional[str]:
    return _download_media(url)
