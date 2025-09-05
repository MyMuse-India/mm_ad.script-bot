# app.py — MyMuse Ad Studio (Production-Grade)
# Optimized for: Performance, Security, Error Handling, Monitoring
from __future__ import annotations
import os
import logging
import tempfile
import time
import traceback
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from contextlib import contextmanager

from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, abort, jsonify, current_app
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
try:
    from flask_wtf.csrf import generate_csrf
except Exception:  # Dev fallback if flask-wtf not installed
    def generate_csrf(*_args, **_kwargs):
        return "dev-csrf-token"

try:
    from flask_limiter.util import get_remote_address
except Exception:  # Dev fallback if flask-limiter not installed
    def get_remote_address(*_args, **_kwargs):
        return "127.0.0.1"

# -----------------------------------------------------------------------------
# Production Configuration & Flask App Setup
# -----------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# Ensure directories exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)

# Production Flask app with optimized settings
app = Flask(
    __name__,
    instance_relative_config=True,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
)

# Production Flask configuration
app.config.update(
    # Security
    SESSION_COOKIE_SECURE=True if os.getenv("FLASK_ENV") == "production" else False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24),
    
    # Performance
    TEMPLATES_AUTO_RELOAD=False if os.getenv("FLASK_ENV") == "production" else True,
    SEND_FILE_MAX_AGE_DEFAULT=timedelta(hours=1),
    
    # File upload limits
    MAX_CONTENT_LENGTH=100 * 1024 * 1024,  # 100MB max file size
)

# -----------------------------------------------------------------------------
# Config & extensions
# -----------------------------------------------------------------------------
from config import Config
app.config.from_object(Config)

from extensions import db, login_manager, csrf, limiter as _limiter

# Production-grade rate limiting with fallback
class _NoLimiter:
    def init_app(self, *a, **k): pass
    def limit(self, *a, **k):
        def deco(f): return f
        return deco

# Enhanced rate limiter with production settings
try:
    limiter = _limiter
    if limiter:
        # Production rate limiting configuration
        limiter.init_app(
            app,
            default_limits=[
                "200 per day",      # Increased from 100
                "50 per hour",      # Increased from 20
                "10 per minute"     # Added per-minute limit
            ],
            key_func=get_remote_address,
            storage_uri="memory://",  # Use memory for production
            strategy="fixed-window"
        )
    else:
        limiter = _NoLimiter()
except Exception as e:
    print(f"Rate limiter initialization failed: {e}")
    limiter = _NoLimiter()

# -----------------------------------------------------------------------------
# Optional modules (keep the app running even if they’re missing)
# -----------------------------------------------------------------------------
try:
    from analysis import sentiment_vader, key_phrases, themes, analyze_agent, analyze_media
except Exception:
    def sentiment_vader(text: str) -> Dict: return {"neg": 0.0, "neu": 1.0, "pos": 0.0, "compound": 0.0}
    def key_phrases(text: str) -> List[str]: return []
    def themes(text: str) -> Dict: return {}

# Transcription helpers
try:
    from transcribe import transcribe_media, transcribe_from_url, download_from_url
except Exception:
    def transcribe_media(path: str) -> str:
        return "Sample transcript (dev fallback). Install ffmpeg + faster-whisper for real transcription."
    def transcribe_from_url(url: str) -> Optional[str]: return None
    def download_from_url(url: str) -> Optional[str]: return None

# Brand-locked generator (your existing agent)
try:
    from generate import generate, generate_variations, generate_variations_text_only
except Exception as e:
    raise RuntimeError(f"generate.py not available or invalid: {e}")

# Auto-scraper service
try:
    from auto_scraper import get_scraper_status, force_scrape_now
except Exception:
    def get_scraper_status():
        return {"error": "Auto-scraper not available"}
    def force_scrape_now():
        return False

# Instagram scraper for training data
try:
    from instagram_scraper import scrape_instagram_posts
except ImportError:
    scrape_instagram_posts = None
    print("Warning: instagram_scraper not available")

# Website scraper for training data
try:
    from mymuse_website_scraper import scrape_and_train
except ImportError:
    scrape_and_train = None
    print("Warning: mymuse_website_scraper not available")

# Reviews index (training via CSV)
try:
    from review_store import ReviewIndex
except Exception:
    class ReviewIndex:
        @classmethod
        def get(cls): return cls
        @classmethod
        def stats(cls): return {"total_docs": 0, "products": []}
        @classmethod
        def samples(cls, n: int = 6): return []
        @classmethod
        def import_csv(cls, file_obj): return {"added": 0, "total": 0}
        @classmethod
        def build(cls): return None
        @classmethod
        def search(cls, product_name: str, query: str, k: int = 6): return []
        @classmethod
        def import_csv_file(cls, path: str): return {"added": 0, "total": 0}
        @classmethod
        def import_csv_dir(cls, path: str): return {"added": 0, "total": 0}

# -----------------------------------------------------------------------------
# Auto-index rebuilding system
# -----------------------------------------------------------------------------
def rebuild_index_automatically():
    """Automatically rebuild the review index from all available data sources"""
    try:
        print("Starting automatic index rebuild...")
        
        # 1. Import reviews CSV
        reviews_csv = os.path.join(BASE_DIR, "data", "mymuse_reviews.csv")
        if os.path.exists(reviews_csv):
            try:
                ReviewIndex.import_csv_file(reviews_csv)
                print("Imported reviews CSV")
            except Exception as e:
                print(f"Could not import reviews CSV: {e}")
        
        # 2. Import features CSV
        features_csv = os.path.join(BASE_DIR, "data", "mymuse_features.csv")
        if os.path.exists(features_csv):
            try:
                ReviewIndex.import_csv_file(features_csv)
                print("Imported features CSV")
            except Exception as e:
                print(f"Could not import features CSV: {e}")
        
        # 3. Auto-scrape website content
        if scrape_and_train:
            try:
                result = scrape_and_train()
                if result and result.get("success"):
                    print("Auto-scraped website content")
            except Exception as e:
                print(f"Could not auto-scrape website: {e}")
        
        # 4. Auto-scrape Instagram content
        if scrape_instagram_posts:
            try:
                result = scrape_instagram_posts("mymuse.in", "mymuse", max_posts=50)
                if result and result.get("success"):
                    print("Auto-scraped Instagram content")
            except Exception as e:
                print(f"Could not auto-scrape Instagram: {e}")
        
        # 5. Import any other CSV files in data directory
        data_dir = os.path.join(BASE_DIR, "data")
        if os.path.isdir(data_dir):
            for filename in os.listdir(data_dir):
                if filename.endswith('.csv') and filename not in ['mymuse_reviews.csv', 'mymuse_features.csv']:
                    csv_path = os.path.join(data_dir, filename)
                    try:
                        ReviewIndex.import_csv_file(csv_path)
                        print(f"Imported {filename}")
                    except Exception as e:
                        print(f"Could not import {filename}: {e}")
        
        # 6. Build the final index
        ReviewIndex.build()
        stats = ReviewIndex.stats()
        print(f"Index rebuild complete: {stats.get('total_docs', 0)} documents, {stats.get('total_terms', 0)} terms")
        
        return True
    except Exception as e:
        print(f"Index rebuild failed: {e}")
        return False

# -----------------------------------------------------------------------------
# Startup tasks
# -----------------------------------------------------------------------------
def run_startup_tasks():
    """Run all startup tasks including index rebuild"""
    try:
        print("Running startup tasks...")
        
        # Rebuild index automatically
        rebuild_index_automatically()
        
        # Set up auto-scraper if available
        try:
            import auto_scraper as _auto_scraper_mod  # type: ignore
            if hasattr(_auto_scraper_mod, 'start_auto_scraper'):
                try:
                    _auto_scraper_mod.start_auto_scraper()
                    print("Auto-scraper started")
                except Exception as e:
                    print(f"Could not start auto-scraper: {e}")
        except Exception:
            pass
        
        print("Startup tasks completed")
    except Exception as e:
        print(f"Startup tasks failed: {e}")

# Run startup tasks when app starts (only if not skipping)
if not os.getenv("SKIP_STARTUP", "").lower() in ("1", "true", "yes", "on"):
    # Run startup tasks in background to avoid blocking port binding
    import threading
    def run_startup_background():
        with app.app_context():
            run_startup_tasks()
    
    startup_thread = threading.Thread(target=run_startup_background, daemon=True)
    startup_thread.start()
    print("Startup tasks started in background thread")
else:
    print("Skipping startup tasks due to SKIP_STARTUP environment variable")

# -----------------------------------------------------------------------------
# Init extensions
# -----------------------------------------------------------------------------
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)

def _cfg(name: str, default: str) -> str:
    return getattr(Config, name, os.getenv(name, default))

try:
    limiter.init_app(app)
    app.config['RATELIMIT_DEFAULT'] = [_cfg("GLOBAL_DAILY_LIMIT","100 per day"), _cfg("GLOBAL_HOURLY_LIMIT","20 per hour")]
    app.config['RATELIMIT_STORAGE_URL'] = "memory://"
    app.config['RATELIMIT_STRATEGY'] = "fixed-window"
except Exception as e:
    print(f"Rate limiter initialization failed: {e}")
    limiter = _NoLimiter()

# -----------------------------------------------------------------------------
# Production-Grade Logging & Monitoring
# -----------------------------------------------------------------------------
# Configure structured logging for production
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
log_format = "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"

# Production logging configuration
logs_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(logs_dir, exist_ok=True)

handlers = [logging.StreamHandler()]
try:
    log_file_path = os.path.join(logs_dir, "app.log")
    file_handler = logging.FileHandler(log_file_path, mode="a")
    handlers.append(file_handler)
    print(f"✅ File logging enabled: {log_file_path}")
except Exception as e:
    print(f"⚠️ File logging disabled: {e}")

logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format=log_format,
    handlers=handlers
)

# Ensure logs directory exists
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

# Structured logger with performance tracking
logger = logging.getLogger("mymuse")

# Performance monitoring
class PerformanceMonitor:
    def __init__(self):
        self.request_times = {}
        self.error_counts = {}
        self.start_time = time.time()
    
    def start_request(self, request_id: str):
        self.request_times[request_id] = time.time()
    
    def end_request(self, request_id: str, success: bool = True):
        if request_id in self.request_times:
            duration = time.time() - self.request_times[request_id]
            logger.info(f"Request {request_id} completed in {duration:.3f}s (success: {success})")
            del self.request_times[request_id]
    
    def log_error(self, error_type: str):
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        logger.error(f"Error count for {error_type}: {self.error_counts[error_type]}")

# Global performance monitor
perf_monitor = PerformanceMonitor()

# CSRF helper for templates
@app.context_processor
def inject_csrf():
    return dict(csrf_token=generate_csrf)

# Production request monitoring middleware
@app.before_request
def before_request():
    """Monitor all requests for performance and security"""
    request_id = f"{request.method}_{request.endpoint}_{int(time.time() * 1000)}"
    request.start_time = time.time()
    request.request_id = request_id
    
    # Log request details
    logger.info(f"Request started: {request_id} - {request.method} {request.path} from {request.remote_addr}")
    
    # Start performance monitoring
    perf_monitor.start_request(request_id)
    
    # Security checks
    if request.method == "POST":
        # Validate CSRF token
        if not request.form.get('csrf_token'):
            logger.warning(f"Missing CSRF token in request: {request_id}")
    
    # Rate limiting check
    if hasattr(request, 'limit_exempt') and request.limit_exempt:
        logger.debug(f"Rate limit exempt request: {request_id}")

@app.after_request
def after_request(response):
    """Log response details and performance metrics"""
    if hasattr(request, 'request_id'):
        request_id = request.request_id
        duration = time.time() - request.start_time
        
        # Log response details
        logger.info(f"Request completed: {request_id} - Status: {response.status_code} - Duration: {duration:.3f}s")
        
        # End performance monitoring
        perf_monitor.end_request(request_id, response.status_code < 400)
        
        # Add performance headers
        response.headers['X-Request-ID'] = request_id
        response.headers['X-Response-Time'] = f"{duration:.3f}s"
    
    return response

# -----------------------------------------------------------------------------
# Models (your existing)
# -----------------------------------------------------------------------------
from models import User, Record

# SQLAlchemy 2.x safe loader
@login_manager.user_loader
def load_user(user_id: str):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return User.query.get(int(user_id))  # type: ignore

login_manager.login_view = "login"

# Ensure DB & warm up review index (+ auto-import CSVs)
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        logger.warning("DB create_all warning: %s", e)
    try:
        # Auto-import CSVs at startup
        csv_path = os.getenv("REVIEW_CSV", "")
        csv_dir  = os.getenv("REVIEW_CSV_DIR", os.path.join(BASE_DIR, "data"))
        try:
            if csv_path:
                ReviewIndex.import_csv_file(csv_path)
            if csv_dir and os.path.isdir(csv_dir):
                ReviewIndex.import_csv_dir(csv_dir)
                # Also import features CSV for product context
                features_csv = os.path.join(csv_dir, "mymuse_features.csv")
                if os.path.exists(features_csv):
                    try:
                        ReviewIndex.import_csv_file(features_csv)
                        logger.info("Imported product features CSV for enhanced context")
                    except Exception as e:
                        logger.warning("Features CSV import failed: %s", e)
            ReviewIndex.build()
        except Exception as e:
            logger.warning("Review CSV import skipped: %s", e)
        ReviewIndex.get()
    except Exception as e:
        logger.warning("ReviewIndex init warning: %s", e)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
# Allow common audio/video so OpenAI Whisper can accept originals (no server conversion).
ALLOWED_MEDIA = {"mp4", "mov", "webm", "mp3", "wav", "m4a"}
def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_MEDIA

def _get_public_user_id() -> int:
    """Return an ID for a public fallback user, creating it if necessary."""
    try:
        public_email = "public@mymuse.local"
        user = User.query.filter_by(email=public_email).first()
        if not user:
            user = User(email=public_email, password_hash=generate_password_hash("public"), is_admin=False, created_at=datetime.utcnow())
            db.session.add(user)
            db.session.commit()
        return int(user.id)
    except Exception:
        # As a last resort, return 0; callers should ensure a valid FK
        return 0

def _current_user_id_or_public() -> int:
    try:
        if getattr(current_user, "is_authenticated", False) and getattr(current_user, "id", None) is not None:
            return int(current_user.id)
    except Exception:
        pass
    return _get_public_user_id()

def _save_record(user_id: int, product: str, transcript: str, generated: str) -> None:
    rec = Record(
        user_id=user_id,
        product_name=product,
        transcript=transcript,
        generated_text=generated,
        created_at=datetime.utcnow()
    )
    db.session.add(rec)
    db.session.commit()

def _require_admin():
    # Auth disabled (Option A): no-op to allow public access
    return None

# -----------------------------------------------------------------------------
# Routes: Auth
# -----------------------------------------------------------------------------
@app.route("/")
def index():
    return redirect(url_for("dashboard"))

@app.route("/signup", methods=["GET","POST"])
@limiter.limit(_cfg("SIGNUP_RATE","12 per minute"))
def signup():
    flash("Signups are disabled. Auth is not required.", "info")
    return redirect(url_for("dashboard"))

@app.route("/login", methods=["GET","POST"])
@limiter.limit(_cfg("LOGIN_RATE","10 per minute"))
def login():
    flash("Login is disabled. Auth is not required.", "info")
    return redirect(url_for("dashboard"))

@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("dashboard"))

# -----------------------------------------------------------------------------
# Routes: Dashboard & Transcription → Generation (SCRIPT-ONLY)
# -----------------------------------------------------------------------------
@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("main/dashboard.html")

@app.route("/transcribe", methods=["POST"])
@limiter.limit(_cfg("TRANSCRIBE_RATE","10 per minute"))  # Increased rate limit
def transcribe_route():
    """Production-grade transcription route with enhanced error handling"""
    start_time = time.time()
    
    try:
        # Input validation with detailed error messages
        product_name = (request.form.get("product_name") or "").strip()
        media_url = (request.form.get("media_url") or "").strip()
        file = request.files.get("media")

        # Enhanced validation
        if not product_name:
            flash("Please choose a product.", "warning")
            return redirect(url_for("dashboard"))
        
        # Validate product name against allowed list
        allowed_products = ["dive+", "link+", "beat", "breeze", "groove+", "edge", "pulse", "flick", "oh! please gel"]
        if product_name not in allowed_products:
            flash("Invalid product selected.", "error")
            return redirect(url_for("dashboard"))

        # Check if either file or URL is provided
        if not file and not media_url:
            flash("Please provide either a media file or URL.", "warning")
            return redirect(url_for("dashboard"))

        transcript_text: Optional[str] = None
        tmp_path: Optional[str] = None

        # 1) Prefer URL if provided
        if media_url:
            transcript_text = transcribe_from_url(media_url)  # returns transcript or None
            if not transcript_text:
                path = download_from_url(media_url)  # returns local path or None
                if path:
                    transcript_text = transcribe_media(path)

        # 2) Fall back to uploaded file
        if not transcript_text and file and file.filename:
            # Enhanced file validation
            if not _allowed_file(file.filename):
                flash("Unsupported file type. Please use: mp4, mov, webm, mp3, wav, m4a", "error")
                return redirect(url_for("dashboard"))
            
            # Secure filename handling
            fname = secure_filename(file.filename)
            if not fname:
                flash("Invalid filename provided.", "error")
                return redirect(url_for("dashboard"))
            
            # Create temporary directory with better security
            tmp_dir = tempfile.mkdtemp(prefix="muse_")
            tmp_path = os.path.join(tmp_dir, fname)
            
            try:
                file.save(tmp_path)
                # Verify file was saved and is readable
                if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
                    raise ValueError("File upload failed")
                
                transcript_text = transcribe_media(tmp_path)
                logger.info(f"File transcription completed: {fname} -> {len(transcript_text or '')} chars")
                
            except Exception as e:
                logger.error(f"File transcription failed: {e}")
                flash("File transcription failed. Please try again.", "error")
                return redirect(url_for("dashboard"))

        # 3) Final fallback with better error handling
        if not transcript_text:
            logger.warning("No transcript generated, using fallback")
            transcript_text = "Sample transcript (dev fallback). Install ffmpeg + faster-whisper for real transcription."

        # Production-grade script generation with enhanced error handling
        logger.info(f"Starting script generation for product: {product_name}")
        
        # Media analysis with error handling
        try:
            media_for_analysis = tmp_path if (tmp_path and os.path.exists(tmp_path)) else None
        except Exception as e:
            logger.warning(f"Media analysis setup failed: {e}")
            media_for_analysis = None
        
        # Enhanced media analysis
        try:
            media_analysis = analyze_media(media_for_analysis, transcript_text)
            sent = media_analysis.get("sentiment", {})
            phrases_list = media_analysis.get("keywords", [])
            theme_map = {"tags": media_analysis.get("themes", [])}
            logger.info(f"Media analysis completed: sentiment={sent}, keywords={len(phrases_list)}, themes={len(theme_map.get('tags', []))}")
        except Exception as e:
            logger.error(f"Media analysis failed: {e}")
            # Fallback analysis
            sent = {"compound": 0.0, "pos": 0.0, "neg": 0.0, "neu": 1.0}
            phrases_list = []
            theme_map = {"tags": []}

        # Enhanced review search with retry logic
        rel_reviews = []
        try:
            rel_reviews = ReviewIndex.search(product_name, transcript_text, k=8)  # Increased from 6
            logger.info(f"Found {len(rel_reviews)} relevant reviews")
        except Exception as e:
            logger.error(f"Review search failed: {e}")
            rel_reviews = []

        # Enhanced script generation parameters
        instagram_mode = request.form.get("instagram_mode") == "on"
        pg13_mode = request.form.get("pg13_mode") == "on"
        genz_mode = request.form.get("genz_mode") == "on"
        
        # Production script generation with comprehensive error handling
        try:
            # Enhanced analysis dict for generate_variations
            analysis_dict = {
                "sentiment": sent,
                "keywords": phrases_list,
                "themes": theme_map.get("tags", []),
                "hook": "",
                "style_tags": [],
                "structure": {},
                "tone": "",
                "genz_mode": genz_mode,
                "transcript_length": len(transcript_text),
                "product_context": product_name
            }
            
            logger.info(f"Calling generate_variations: product={product_name}, transcript_length={len(transcript_text)}, modes=[instagram:{instagram_mode}, pg13:{pg13_mode}, genz:{genz_mode}]")
            
            # Performance monitoring for script generation
            gen_start_time = time.time()
            result = generate_variations(
                product_name, 
                transcript_text, 
                analysis_dict, 
                rel_reviews=rel_reviews, 
                instagram_mode=instagram_mode, 
                pg13_mode=pg13_mode, 
                genz_mode=genz_mode
            )
            gen_duration = time.time() - gen_start_time
            
            logger.info(f"Script generation completed in {gen_duration:.3f}s: {len(result.get('variations', []))} variations")
            
        except Exception as e:
            logger.error(f"Script generation failed: {e}")
            perf_monitor.log_error("script_generation")
            result = {"variations": [], "summary": "Generation failed due to system error"}
        
        # Enhanced result processing
        variations = result.get("variations", [])
        if variations:
            generated = (variations[0].get("text", "") or "").strip() or "No output generated."
            evaluation = variations[0].get("evaluation", {})
            summary = result.get("summary", "")
            logger.info(f"Script generation successful: {len(variations)} variations, first_script_length={len(generated)}")
        else:
            generated = "Script generation failed. Please try again."
            evaluation = None
            summary = "No variations generated"
            logger.warning("No script variations generated")

        # Enhanced record saving with retry logic
        try:
            _save_record(_current_user_id_or_public(), product_name, transcript_text, generated)
            logger.info(f"Record saved successfully for user {current_user.id}")
        except Exception as e:
            logger.error(f"Failed to save record: {e}")
            perf_monitor.log_error("database_save")
            # Don't fail the entire request if saving fails

        # Calculate total processing time
        total_duration = time.time() - start_time
        logger.info(f"Transcription route completed in {total_duration:.3f}s")

        # Success response with enhanced data
        flash("Transcription and script generated successfully!", "success")
        return render_template("main/dashboard.html",
                               product_name=product_name,
                               transcript=transcript_text,
                               generated=generated,
                               evaluation=evaluation,
                               variations=variations,
                               processing_time=f"{total_duration:.2f}s")
                               
    except Exception as e:
        # Enhanced error handling with detailed logging
        error_msg = f"Transcription failed: {str(e)}"
        logger.exception(f"Critical error in transcription route: {error_msg}")
        perf_monitor.log_error("transcription_critical")
        
        # User-friendly error message
        flash("Something went wrong while processing your media. Please try again.", "error")
        return render_template("main/dashboard.html", error=error_msg)
        
    finally:
        # Enhanced cleanup with error handling
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
                logger.debug(f"Temporary file removed: {tmp_path}")
            except Exception as e:
                logger.warning(f"Failed to remove temp file {tmp_path}: {e}")
            
            try:
                tmp_dir = os.path.dirname(tmp_path)
                if os.path.exists(tmp_dir):
                    os.rmdir(tmp_dir)
                    logger.debug(f"Temporary directory removed: {tmp_dir}")
            except Exception as e:
                logger.warning(f"Failed to remove temp directory {tmp_dir}: {e}")

# -----------------------------------------------------------------------------
# Route: Generate from Transcript (Step 3)
# -----------------------------------------------------------------------------
@app.route("/generate", methods=["POST"])
@limiter.limit(_cfg("GENERATE_RATE","5 per minute"))
def generate_route():
    product_name = (request.form.get("product_name") or "").strip()
    transcript_text = (request.form.get("transcript_text") or "").strip()
    output_style = None
    if not product_name:
        flash("Please provide a product name.", "warning")
        return redirect(url_for("dashboard"))
    if not transcript_text:
        flash("Please provide a transcript or transcribe a media file first.", "warning")
        return redirect(url_for("dashboard"))

    try:
        # Agent 1 for given transcript only (no media here)
        analysis = analyze_agent(transcript_text)
        sent = analysis.get("sentiment", {})
        phrases_list = analysis.get("keywords", [])
        theme_map = {"tags": analysis.get("themes", [])}
        try:
            rel_reviews = ReviewIndex.search(product_name, transcript_text, k=6)
        except Exception:
            rel_reviews = []
        
        # Generate script with product integration
        instagram_mode = request.form.get("instagram_mode") == "on"
        pg13_mode = request.form.get("pg13_mode") == "on"
        genz_mode = request.form.get("genz_mode") == "on"
        
        try:
            # Use full generator to get primary script + 10 variations
            result = generate(
                product_name,
                transcript_text,
                sent,
                phrases_list,
                theme_map,
                rel_reviews=rel_reviews,
                output_style=None,
                gen_z=genz_mode,
            )
            generated = (result.get("generated_script") or "").strip() or "No output."
            variations = result.get("variations", [])
            summary = ""
        except Exception as e:
            logger.error(f"Error in generate_variations: {e}")
            generated = "Generation failed"
            variations = []
            summary = ""

        try:
            # Save the generated script
            _save_record(_current_user_id_or_public(), product_name, transcript_text, generated)
        except Exception as e:
            logger.warning("Could not save record: %s", e)

        flash("Script generated successfully!", "success")
        return render_template("main/dashboard.html",
                               product_name=product_name,
                               transcript=transcript_text,
                               generated=generated,
                               variations=variations)
    except Exception as e:
        logger.exception("Error in /generate: %s", e)
        flash("Something went wrong while generating your script.", "error")
        return redirect(url_for("dashboard"))

# -----------------------------------------------------------------------------
# Route: Auto-Detect Product + Generate (Step 2)
# -----------------------------------------------------------------------------
@app.route("/auto-detect-product", methods=["POST"])
@limiter.limit(_cfg("GENERATE_RATE","5 per minute"))
def auto_detect_product():
    transcript_text = (request.form.get("transcript_text") or "").strip()
    if not transcript_text:
        flash("Please provide a transcript.", "warning")
        return redirect(url_for("dashboard"))

    try:
        # Auto-detect product from transcript content
        product_name = _detect_product_from_transcript(transcript_text)
        
        # Agent 1 for given transcript only (no media here)
        analysis = analyze_agent(transcript_text)
        sent = analysis.get("sentiment", {})
        phrases_list = analysis.get("keywords", [])
        theme_map = {"tags": analysis.get("themes", [])}
        try:
            rel_reviews = ReviewIndex.search(product_name, transcript_text, k=6)
        except Exception:
            rel_reviews = []
        
        # Generate script with detected product
        instagram_mode = request.form.get("instagram_mode") == "on"
        pg13_mode = request.form.get("pg13_mode") == "on"
        genz_mode = request.form.get("genz_mode") == "on"
        
        try:
            result = generate_variations(product_name, transcript_text, analysis, rel_reviews=rel_reviews, instagram_mode=instagram_mode, pg13_mode=pg13_mode, genz_mode=genz_mode)
            generated = (result.get("variations", [{}])[0].get("text", "") or "").strip() or "No output."
            variations = result.get("variations", [])
            summary = result.get("summary", "")
        except Exception as e:
            logger.error(f"Error in generate_variations: {e}")
            generated = "Generation failed"
            variations = []
            summary = ""

        try:
            # Save the generated script
            _save_record(_current_user_id_or_public(), product_name, transcript_text, generated)
        except Exception as e:
            logger.warning("Could not save record: %s", e)

        flash(f"Product auto-detected: {product_name}. Script generated successfully!", "success")
        return render_template("main/dashboard.html",
                               product_name=product_name,
                               transcript=transcript_text,
                               generated=generated,
                               variations=variations)
    except Exception as e:
        logger.exception("Error in /auto-detect-product: %s", e)
        flash("Something went wrong while auto-detecting product and generating script.", "error")
        return redirect(url_for("dashboard"))

# -----------------------------------------------------------------------------
# Route: Generate Variations Only (Step 3)
# -----------------------------------------------------------------------------
@app.route("/generate-variations-only", methods=["POST"])
@limiter.limit(_cfg("GENERATE_RATE","5 per minute"))
def generate_variations_only():
    script_text = (request.form.get("script_text") or "").strip()
    if not script_text:
        flash("Please provide a script to generate variations from.", "warning")
        return redirect(url_for("dashboard"))

    try:
        # Generate variations without product integration
        instagram_mode = request.form.get("instagram_mode") == "on"
        pg13_mode = request.form.get("pg13_mode") == "on"
        genz_mode = request.form.get("genz_mode") == "on"
        
        try:
            # Use text-only variations function
            result = generate_variations_text_only(script_text, {"genz_mode": genz_mode}, count=10, pg13_mode=pg13_mode, genz_mode=genz_mode)
            variations = result.get("variations", [])
            summary = result.get("summary", "")
        except Exception as e:
            logger.error(f"Error in generate_variations_text_only: {e}")
            variations = []
            summary = "Generation failed"

        flash("10 variations generated successfully!", "success")
        return render_template("main/dashboard.html",
                               transcript="",
                               generated="",
                               variations=variations)
    except Exception as e:
        logger.exception("Error in /generate-variations-only: %s", e)
        flash("Something went wrong while generating variations.", "error")
        return redirect(url_for("dashboard"))

# -----------------------------------------------------------------------------
# Route: Generate 10 Variations
# -----------------------------------------------------------------------------
@app.route("/generate_variations", methods=["POST"])
@limiter.limit(_cfg("GENERATE_RATE","5 per minute"))
def generate_variations_route():
    product_name = (request.form.get("product_name") or "").strip()
    transcript_text = (request.form.get("transcript_text") or "").strip()
    if not product_name:
        flash("Please provide a product name.", "warning")
        return redirect(url_for("dashboard"))
    if not transcript_text:
        flash("Please provide a transcript or transcribe a media file first.", "warning")
        return redirect(url_for("dashboard"))

    try:
        analysis = analyze_agent(transcript_text)
        instagram_mode = request.form.get("instagram_mode") == "on"
        pg13_mode = request.form.get("pg13_mode") == "on"
        genz_mode = request.form.get("genz_mode") == "on"
        try:
            rel_reviews = ReviewIndex.search(product_name, transcript_text, k=8)
        except Exception:
            rel_reviews = []
        payload = generate_variations(product_name, transcript_text, analysis, rel_reviews=rel_reviews, instagram_mode=instagram_mode, pg13_mode=pg13_mode, genz_mode=genz_mode)
        variations = payload.get("variations", [])
        summary = payload.get("summary", "")
        flash("Generated variations successfully.", "success")
        return render_template("main/dashboard.html",
                               product_name=product_name,
                               transcript=transcript_text,
                               variations=variations,
                               summary=summary)
    except Exception as e:
        logger.exception("Error in /generate_variations: %s", e)
        flash("Something went wrong while generating variations.", "error")
        return render_template("main/dashboard.html")

# -----------------------------------------------------------------------------
# Route: Generate 10 Variations — Text Only (Step 3)
# -----------------------------------------------------------------------------
@app.route("/generate_variations_text_only", methods=["POST"])
@limiter.limit(_cfg("GENERATE_RATE","5 per minute"))
def generate_variations_text_only_route():
    transcript_text = (request.form.get("transcript_text_textonly") or "").strip()
    instagram_mode = request.form.get("instagram_mode_textonly") == "on"
    if not transcript_text:
        flash("Please paste a transcript/script.", "warning")
        return redirect(url_for("dashboard"))

    try:
        analysis = analyze_agent(transcript_text)
        pg13_mode = request.form.get("pg13_mode_textonly") == "on"
        genz_mode = request.form.get("genz_mode_textonly") == "on"
        payload = generate_variations_text_only(
            transcript_text=transcript_text,
            analysis=analysis,
            count=10,
            instagram_mode=instagram_mode,
            pg13_mode=pg13_mode,
            genz_mode=genz_mode,
        )
        variations = payload.get("variations", [])
        summary = payload.get("summary", "")
        flash("Generated text-only variations successfully.", "success")
        return render_template("main/dashboard.html",
                               transcript=transcript_text,
                               variations=variations,
                               summary=summary)
    except Exception as e:
        logger.exception("Error in /generate_variations_text_only: %s", e)
        flash("Something went wrong while generating variations.", "error")
        return render_template("main/dashboard.html")

# -----------------------------------------------------------------------------
# Routes: Admin — Reviews (CSV training)
# -----------------------------------------------------------------------------
@app.route("/admin/reviews", methods=["GET"])
def admin_reviews():
    stats = ReviewIndex.stats()
    samples = ReviewIndex.samples(6)
    return render_template("main/admin_reviews.html", stats=stats, samples=samples)

@app.route("/admin/reviews/upload", methods=["POST"])
def admin_reviews_upload():
    f = request.files.get("csv_file")
    if not f or not f.filename.lower().endswith(".csv"):
        flash("Please upload a CSV with headers: product_name,text", "warning")
        return redirect(url_for("admin_reviews"))
    try:
        info = ReviewIndex.import_csv(f)
        ReviewIndex.build()
        flash(f"Imported {info.get('added',0)} reviews. Total: {info.get('total',0)}.", "success")
    except Exception as e:
        logging.exception("CSV import failed: %s", e)
        flash(f"Import failed: {e}", "error")
    return redirect(url_for("admin_reviews"))

# -----------------------------------------------------------------------------
# Route: Auto-Scraper Status & Control
# -----------------------------------------------------------------------------
@app.route("/admin/auto-scraper", methods=["GET", "POST"])
def admin_auto_scraper():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "force_scrape":
            success = force_scrape_now()
            if success:
                flash("Manual scrape triggered successfully.", "success")
            else:
                flash("Manual scrape failed.", "error")
        return redirect(url_for("admin_auto_scraper"))
    
    status = get_scraper_status()
    return render_template("main/admin_auto_scraper.html", status=status)

# -----------------------------------------------------------------------------
# Route: Website Scraping
# -----------------------------------------------------------------------------
@app.route('/admin/website-scrape', methods=['GET', 'POST'])
def admin_website_scrape():
    if request.method == 'POST':
        if not scrape_and_train:
            flash('Website scraper not available. Please install required dependencies.', 'error')
            return redirect(url_for('admin_website_scrape'))
        
        try:
            # Get form data
            url = request.form.get('url', 'https://mymuse.in/collections/deal-of-the-day')
            product_name = request.form.get('product_name', 'mymuse')
            
            # Run the scraper
            result = scrape_and_train(url, product_name)
            
            if result.get('success'):
                # Auto-import into review index
                try:
                    from review_store import ReviewIndex
                    info = ReviewIndex.import_csv_file(result['csv_path'])
                    ReviewIndex.build()
                    flash(f'Successfully scraped {result["training_examples"]} training examples and imported into review index!', 'success')
                except Exception as e:
                    flash(f'Scraping successful but import failed: {str(e)}', 'warning')
            else:
                flash(f'Scraping failed: {result.get("error", "Unknown error")}', 'error')
                
        except Exception as e:
            flash(f'Error during scraping: {str(e)}', 'error')
    
    return render_template('main/admin_website_scrape.html')

# -----------------------------------------------------------------------------
# Route: Instagram Scraping
# -----------------------------------------------------------------------------
@app.route('/admin/instagram-scrape', methods=['GET', 'POST'])
def admin_instagram_scrape():
    if request.method == 'POST':
        try:
            # Get form data
            username = request.form.get('username', 'mymuse.in')
            product_name = request.form.get('product_name', 'mymuse')
            max_posts = int(request.form.get('max_posts', 50))
            
            # Import and run Instagram scraper
            try:
                from instagram_scraper import scrape_instagram_posts
                result = scrape_instagram_posts(username, product_name, max_posts)
                
                if result.get('success'):
                    # Auto-import into review index
                    try:
                        from review_store import ReviewIndex
                        info = ReviewIndex.import_csv_file(result['csv_path'])
                        ReviewIndex.build()
                        flash(f'Successfully scraped {result["training_examples"]} Instagram posts and imported into review index!', 'success')
                    except Exception as e:
                        flash(f'Instagram scraping successful but import failed: {str(e)}', 'warning')
                else:
                    flash(f'Instagram scraping failed: {result.get("error", "Unknown error")}', 'error')
                    
            except ImportError:
                flash('Instagram scraper not available. Please install required dependencies.', 'error')
                
        except Exception as e:
            flash(f'Error during Instagram scraping: {str(e)}', 'error')
    
    return render_template('main/admin_instagram_scrape.html')

# -----------------------------------------------------------------------------
# Error handlers
# -----------------------------------------------------------------------------
@app.errorhandler(403)
def forbidden(e):
    flash("You are not allowed to access that page.", "error")
    return redirect(url_for("dashboard"))

@app.errorhandler(404)
def not_found(e):
    flash("Page not found.", "warning")
    return redirect(url_for("dashboard"))

@app.errorhandler(429)
def ratelimited(e):
    flash("You’re going too fast — please try again in a moment.", "warning")
    return redirect(url_for("dashboard"))

@app.errorhandler(500)
def server_error(e):
    flash("Server error. Please try again.", "error")
    return redirect(url_for("dashboard"))

# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Prefer Render's PORT; fallback to FLASK_PORT, then 10000
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port_env = os.getenv("PORT") or os.getenv("FLASK_PORT") or "10000"
    port = int(port_env)
    debug = (os.getenv("FLASK_DEBUG", "false").lower() in ("1","true","yes","on"))
    app.run(host=host, port=port, debug=debug)

# -----------------------------------------------------------------------------
# Product Auto-Detection Engine
# -----------------------------------------------------------------------------
def _detect_product_from_transcript(transcript_text: str) -> str:
    """Intelligently detect MyMuse product from transcript content"""
    if not transcript_text:
        return "dive+"  # Default fallback
    
    transcript_lower = transcript_text.lower()
    
    # Direct product mentions
    product_keywords = {
        "dive+": ["dive", "dive+", "dive plus", "pebble", "egg-shaped"],
        "link+": ["link", "link+", "link plus", "dual", "couples", "long distance"],
        "beat": ["beat", "stroker", "compact", "travel", "discreet"],
        "breeze": ["breeze", "air pulse", "revolutionary", "different sensation"],
        "groove+": ["groove", "groove+", "groove plus", "wand", "flexible"],
        "edge": ["edge", "stroker", "vibrating", "penis"],
        "pulse": ["pulse", "full body", "massager", "pointed"],
        "flick": ["flick", "mini", "bullet", "quick"],
        "oh! please gel": ["gel", "lube", "lubricant", "oh please", "preparation"]
    }
    
    # Score each product based on keyword matches
    product_scores = {}
    for product, keywords in product_keywords.items():
        score = 0
        for keyword in keywords:
            if keyword in transcript_lower:
                score += 1
                # Bonus for exact matches
                if keyword in transcript_lower.split():
                    score += 2
        product_scores[product] = score
    
    # Find the product with highest score
    best_product = max(product_scores.items(), key=lambda x: x[1])
    
    # If no clear match, use neutral context clues (no travel bias)
    if best_product[1] == 0:
        if any(word in transcript_lower for word in ["couples", "partner", "long distance", "distance"]):
            return "link+"  # Couples-focused without implying travel
        elif any(word in transcript_lower for word in ["quick", "fast", "discreet", "compact"]):
            return "beat"   # Quick sessions / discreet
        elif any(word in transcript_lower for word in ["wand", "flexible", "massage", "knot", "tension"]):
            return "groove+"  # Wand vibes for relaxation/ritual
        elif any(word in transcript_lower for word in ["air pulse", "suction", "different sensation"]):
            return "breeze" # Unique technology
        else:
            return "dive+"  # Default to most popular
    
    return best_product[0]
