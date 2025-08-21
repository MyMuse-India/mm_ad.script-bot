# MyMuse Ad Script Generator - Architecture Document

## 1. Basic Info
- **Agent / Workflow Name**: MyMuse Ad Script Generator
- **Date Created**: August 19, 2025
- **Date Updated**: August 20, 2025
- **Status**: Prototype (working end-to-end locally)

## 2. Purpose
- **What it does**: Two-agent pipeline that converts short-form videos (Reels/Shorts) into brand-locked MyMuse ad scripts by transcribing audio and mirroring tone/context with precise product swaps and feature upgrades.
- **Why**: Automates scriptwriting with strict brand voice and format, preserving original vibe while swapping in correct MyMuse product terms and real features.

## 3. Inputs
- **Trigger**: Manual upload or media URL via web dashboard
- **Collected**:
  - Product name (required)
  - Media file: mp4, mov, webm, mp3, wav, m4a
  - Media URL (optional)
- **Format**: Multipart form + text inputs (CSV training is ingested at boot)

## 4. Processing / Core Logic
- **Flow (story bullets)**:
  - User opens `dashboard` → selects MyMuse product → uploads media or pastes URL → clicks Transcribe
  - Agent A (Transcriber)
    - Ensures audio is 16kHz mono WAV
    - Uses faster-whisper (local) with VAD; auto-detects and downloads model if needed
    - Falls back to OpenAI Whisper REST if configured
  - Analysis Engine
    - VADER sentiment
    - Key phrases (token frequency heuristic)
    - Theme tags (travel, calm, playful, etc.)
  - Review Index (TF-IDF)
    - Loads CSV(s) at app start; prioritizes reviews matching aliases of selected product
  - Agent B (Copywriter)
    - Prompt is built with strict case rules and brand constraints
    - Model call chain: Groq → OpenAI → local fallback
    - Post-processing:
      - Product swap for non-MyMuse placeholders
      - Shape/descriptor corrections per product facts (e.g., "pebble-shaped" for Dive+; ban "wand")
      - Transcript-type detection with case-based enforcement:
        - Case 1 (Casual): keep words EXACT, only product name swap
        - Case 2 (Feature-heavy): "natural flow rewrite" that upgrades fake features to real ones, keeps flow, and ends with CTA
        - Case 3 (Sexual): mirror sexual tone, then natural pivot to pleasure-focused features
      - Case 2 hard enforcement: strict feature replacements:
        - "18 speed modes" → "10+ vibration modes"
        - "11 inches" → "compact design"
        - "black and red color" → "signature MyMuse colors"
      - For Case 2, output is transformed into a natural, flowing one-on-one dialog while retaining the transcript's intent and structure cues; CTA appended
  - Render results on dashboard with copy buttons; record saved to DB

- **AI Models Used**:
  - Transcription: faster-whisper (Systran faster-whisper-small), OpenAI Whisper-1 (optional)
  - Generation: Groq (Llama-3.1-70B) primary → OpenAI (GPT-4o-mini) fallback → local template fallback

## 5. Outputs
- **Destination**: Web dashboard (right pane)
- **Format**:
  - Default: dialog (single speaker "ACTOR/MODEL:" lines)
  - Case 2: natural, flowing rewrite that upgrades only features; ends with "Tap to shop MyMuse {product}."
  - Transcript text displayed for reference
- **Audience**: Marketing team, content creators, social managers

## 6. Data Flow (High-Level)
- Input (product + media/URL)
- Transcription (FFmpeg normalize → faster-whisper/OpenAI)
- Analysis (sentiment, phrases, themes)
- Review Search (TF-IDF on CSV)
- Prompt Build (brand rules + case rules + context)
- LLM Generation (Groq → OpenAI → local)
- Post-Processing (swap, shape fix, case enforcement)
- Store (SQLite) → Display (dashboard)

## 7. Hosting & Infrastructure
- **Where it runs**: Local Flask dev server
- **Storage**:
  - SQLite (`instance/app.db`) for user and generated scripts
  - HF cache under user home for Whisper models
  - CSV reviews in `data/` auto-imported at startup into in-memory TF-IDF index
- **Trigger**: User action on dashboard (no schedulers/webhooks yet)

## 8. Maintenance Notes
- **Known Limitations**:
  - Groq path requires `GROQ_API_KEY`; otherwise falls back to OpenAI
  - Windows HF cache warns about symlinks (safe to ignore; degraded cache)
  - Heuristic transcript-type detection (now prioritizes feature-heavy over sexual when both appear)
  - No diarization; dialog forced to single speaker by design
- **Dependencies**:
  - Python 3.10.x venv
  - Flask, Flask-Login, Flask-WTF, Flask-Limiter, SQLAlchemy
  - faster-whisper, onnxruntime, huggingface_hub
  - requests, nltk, scikit-learn
  - imageio-ffmpeg (bundled ffmpeg autodiscovery)
  - Optional: OpenAI + Groq API keys
- **Env Vars** (commonly used):
  - `WHISPER_MODEL` (e.g., small), `WHISPER_COMPUTE_TYPE` (e.g., int8)
  - `TRANSCRIBE_BACKEND` (openai|local), `OPENAI_API_KEY`, `GROQ_API_KEY`
  - `FFMPEG_BIN` (optional; otherwise auto-discovered via imageio-ffmpeg)
  - `REVIEW_CSV` or `REVIEW_CSV_DIR` (defaults to `data/`)
  - `FLASK_HOST`/`FLASK_PORT`/`FLASK_DEBUG`
  - `ALLOW_ADULT` and `INTIMACY_MODE` (brand safety)
- **How to update/change**:
  - Reviews: drop CSVs in `data/` (headers: `product_name,text`); restart app
  - Product facts/aliases: edit `generate.py` (`PRODUCT_FACTS`, `PRODUCT_ALIASES`)
  - Case rules/prompt: edit `_build_prompt` in `generate.py`
  - Feature enforcement and natural rewrite: `_enforce_case2_structure` in `generate.py`
  - Transcription backend: set `TRANSCRIBE_BACKEND=openai` + provide `OPENAI_API_KEY`
  - FFmpeg: rely on bundled `imageio-ffmpeg` or set `FFMPEG_BIN` to system ffmpeg

## Key Updates Implemented (August 20, 2025)
- **Transcription Fixed**: Automatic ffmpeg discovery via `imageio-ffmpeg` and Whisper small model
- **Case Detection Reordered**: Prefers "feature_heavy" when features are present (e.g., "18 speed modes", "11 inches")
- **Case 2 Strict Enforcement**: Natural-flow rewrite with exact feature swaps and mandatory CTA
- **Default Output Style**: Single-speaker dialog; output-style selector removed from UI
- **Product Shape Enforcement**: Dive+ "pebble-shaped"; bans "wand" and other incorrect descriptors
- **Post-Gen Swap Refined**: Avoids over-replacing common words; precise product nicknames handled
- **System Prompt Tightened**: Preserves tone and flow while swapping products
- **Dashboard Flow**: Transcription + analysis + generation shown clearly; records saved to DB

## Quick Start
1. **Setup**: `python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt`
2. **Run**: `python app.py` (opens http://127.0.0.1:5000)
3. **Test**: Upload a short video, select product, click Transcribe
4. **Customize**: Edit `generate.py` for product facts, aliases, and case rules

## File Structure
```
mymuse_copy_pro/
├── app.py              # Flask routes + transcription → generation pipeline
├── generate.py         # Core script generation + case-based rules + post-processing
├── transcribe.py       # Audio processing + Whisper integration + ffmpeg auto-discovery
├── analysis.py         # Sentiment + key phrases + themes + transcript type detection
├── review_store.py     # TF-IDF review index + CSV import + product search
├── models.py           # SQLAlchemy models (User, Record)
├── config.py           # Flask config + environment variables
├── extensions.py       # Flask extensions (db, login, csrf, limiter)
├── data/               # CSV reviews + auto-scraped training data
├── templates/          # Dashboard + auth templates
├── static/             # CSS + JS for dashboard
└── instance/           # SQLite database + app state
```
