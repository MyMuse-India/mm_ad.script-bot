from __future__ import annotations
import re
from typing import Dict, List, Tuple

# --------------------
# Sentiment (VADER)
# --------------------
def sentiment_vader(text: str) -> Dict[str, float]:
    try:
        from nltk.sentiment import SentimentIntensityAnalyzer
        sia = SentimentIntensityAnalyzer()
        return sia.polarity_scores(text or "")
    except Exception:
        # Fallback neutral
        return {"neg": 0.0, "neu": 1.0, "pos": 0.0, "compound": 0.0}


# --------------------
# Simple key phrase extractor (heuristic)
# --------------------
def key_phrases(text: str, max_phrases: int = 10) -> List[str]:
    if not text:
        return []
    tokens = re.findall(r"[A-Za-z][A-Za-z+'-]{2,}", text)
    stop = {
        "the","and","for","with","this","that","you","are","was","but","have","has","had",
        "i","a","to","it","on","in","of","is","be","as","at","by","or","we","me","my",
        "your","our","they","them","their","from","an","so","not","do","did","just","love",
    }
    freq: Dict[str,int] = {}
    for t in tokens:
        lt = t.lower()
        if lt in stop:
            continue
        freq[lt] = freq.get(lt, 0) + 1
    ranked = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    return [k for k,_ in ranked[:max_phrases]]


# --------------------
# Theme tags (very light heuristic)
# --------------------
def themes(text: str) -> Dict[str, List[str]]:
    t = (text or "").lower()
    tags: List[str] = []
    if any(w in t for w in ["airport","flight","security","boarding","gate","plane","luggage","baggage"]):
        tags.append("travel")
    if any(w in t for w in ["morning","routine","coffee","breakfast"]):
        tags.append("morning_routine")
    if any(w in t for w in ["night","bed","candle","wine","mood"]):
        tags.append("evening_mood")
    if any(w in t for w in ["fun","playful","flirty","adventure","vibe"]):
        tags.append("playful")
    if any(w in t for w in ["calm","slow","soft","quiet"]):
        tags.append("calm")
    return {"tags": tags}


# --------------------
# Hook detection and structure mapping (lightweight)
# --------------------
def detect_hook(text: str) -> str:
    """Return the opening hook (first engaging beat).
    Heuristic: first sentence or first ~120 chars of first line.
    """
    if not text:
        return ""
    # Prefer first line break as a cue; else first sentence end punctuation
    first_line = (text.splitlines()[0] if text.splitlines() else text).strip()
    if not first_line:
        first_line = text.strip()
    # Sentence split (very light)
    parts = re.split(r"(?<=[.!?])\s+", first_line)
    hook = parts[0] if parts and parts[0] else first_line
    return (hook[:120]).strip()


def structure_map(text: str) -> Dict[str, List[str]]:
    """Identify rough structure: hook, setup, proof, offer, CTA.
    Returns keys with extracted snippets (may be empty).
    """
    t = (text or "").strip()
    lines = [l.strip() for l in t.splitlines() if l.strip()]
    hook = detect_hook(t)
    setup: List[str] = []
    proof: List[str] = []
    offer: List[str] = []
    cta: List[str] = []
    for l in lines[1:]:
        low = l.lower()
        if any(k in low for k in ["review", "rated", "customers", "proof", "because", "since", "tested", "loved"]):
            proof.append(l)
        elif any(k in low for k in ["use", "works", "how", "here's", "here’s", "why"]):
            setup.append(l)
        elif any(k in low for k in ["off", "%", "discount", "deal", "today only", "now", "limited"]):
            offer.append(l)
        elif any(k in low for k in ["tap", "shop", "buy", "link", "bio", "cta", "learn more"]):
            cta.append(l)
    return {
        "hook": [hook] if hook else [],
        "setup": setup[:3],
        "proof": proof[:3],
        "offer": offer[:2],
        "cta": cta[:2],
    }


def reading_level(text: str) -> Dict[str, float]:
    """Approximate readability (Flesch-Kincaid style, rough)."""
    t = (text or "").strip()
    if not t:
        return {"grade": 8.0}
    sentences = max(1, len(re.split(r"[.!?]+", t)))
    words = re.findall(r"[A-Za-z]+", t)
    word_count = max(1, len(words))
    # Rough syllable estimate: count vowel groups
    syllables = 0
    for w in words:
        syl = max(1, len(re.findall(r"[aeiouyAEIOUY]+", w)))
        syllables += syl
    # Flesch-Kincaid Grade (approx)
    grade = 0.39 * (word_count / sentences) + 11.8 * (syllables / word_count) - 15.59
    return {"grade": round(max(0.0, grade), 1)}


# --------------------
# Agent 1: multimodal-style analyzer (transcript-proxy)
# --------------------
def analyze_agent(transcript_text: str) -> Dict:
    sent = sentiment_vader(transcript_text)
    phrases = key_phrases(transcript_text, max_phrases=8)
    th = themes(transcript_text)
    # Map compound to coarse tone
    comp = float(sent.get("compound", 0.0))
    tone = "positive" if comp >= 0.25 else ("neutral" if comp > -0.25 else "reassuring")
    # Speaker style cues (heuristic)
    st: List[str] = []
    lower = (transcript_text or "").lower()
    if any(w in lower for w in ["ready","let's","let us","let’s","gotta","love","time for"]):
        st.append("energetic")
    if any(w in lower for w in ["calm","slow","soft","quiet"]):
        st.append("calm")
    if any(w in lower for w in ["playful","flirty","fun","adventure"]):
        st.append("playful")
    # Output schema for Agent 2
    return {
        "tone": tone,
        "sentiment": sent,
        "keywords": phrases,
        "themes": th.get("tags", []),
        "style_tags": st,
        "hook": detect_hook(transcript_text),
        "structure": structure_map(transcript_text),
        "reading": reading_level(transcript_text),
    }


# --------------------
# Agent 1 (media): audio-driven features + text
# --------------------
def analyze_media(media_path: str | None, transcript_text: str) -> Dict:
    analysis = analyze_agent(transcript_text)
    if not media_path:
        return analysis
    try:
        import soundfile as sf
        import numpy as np
        data, sr = sf.read(media_path, always_2d=False)
        x = data.astype("float32") if hasattr(data, "dtype") else np.array(data, dtype="float32")
        if x.ndim == 2:
            x = x.mean(axis=1)
        if x.size == 0:
            return analysis
        # RMS energy
        rms = float(np.sqrt(np.mean(x**2)))
        # Zero-crossing rate (simple tempo/activity proxy)
        zcr = float(((x[:-1] * x[1:]) < 0).sum() / max(1, len(x)-1))
        # Classify
        energy = "high" if rms > 0.2 else ("medium" if rms > 0.05 else "low")
        tempo_like = "fast" if zcr > 0.08 else ("medium" if zcr > 0.03 else "slow")
        tags = set(analysis.get("style_tags", []))
        if energy == "high":
            tags.add("energetic")
        if tempo_like == "slow":
            tags.add("calm")
        analysis.update({
            "audio": {"rms": rms, "zcr": zcr, "energy": energy, "tempo": tempo_like},
            "style_tags": sorted(tags),
        })
        return analysis
    except Exception:
        return analysis


