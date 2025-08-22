# app.py — MyMuse Ad Studio (tiny hooks: transcription + review index into agent)
from __future__ import annotations
import os, logging, tempfile
from datetime import datetime
from typing import Optional, Dict, List

from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, abort
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf.csrf import generate_csrf

# -----------------------------------------------------------------------------
# Paths & Flask app (explicit template/static folders for reliability)
# -----------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(
    __name__,
    instance_relative_config=True,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)

# -----------------------------------------------------------------------------
# Config & extensions
# -----------------------------------------------------------------------------
from config import Config
app.config.from_object(Config)

from extensions import db, login_manager, csrf, limiter as _limiter

# Limiter may be missing or already inited; make a no-op wrapper if needed
class _NoLimiter:
    def init_app(self, *a, **k): pass
    def limit(self, *a, **k):
        def deco(f): return f
        return deco
limiter = _limiter or _NoLimiter()

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

# Instagram scraper for training data
try:
    from mymuse_website_scraper import scrape_and_train
except ImportError:
    scrape_and_train = None
    print("Warning: mymuse_website_scraper not available")

# Auto-scraper service
try:
    from auto_scraper import get_scraper_status, force_scrape_now
except Exception:
    def get_scraper_status():
        return {"error": "Auto-scraper not available"}
    def force_scrape_now():
        return False

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

# -----------------------------------------------------------------------------
# Init extensions
# -----------------------------------------------------------------------------
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)

def _cfg(name: str, default: str) -> str:
    return getattr(Config, name, os.getenv(name, default))

try:
    limiter.init_app(
        app,
        default_limits=[_cfg("GLOBAL_DAILY_LIMIT","100 per day"), _cfg("GLOBAL_HOURLY_LIMIT","20 per hour")],
        key_func=lambda: request.remote_addr or "anon"
    )
except Exception:
    pass

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=getattr(logging, (os.getenv("LOG_LEVEL") or "INFO").upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
)
logger = logging.getLogger("mymuse")

# CSRF helper for templates
@app.context_processor
def inject_csrf():
    return dict(csrf_token=generate_csrf)

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
    if not (current_user.is_authenticated and getattr(current_user, "is_admin", False)):
        abort(403)

# -----------------------------------------------------------------------------
# Routes: Auth
# -----------------------------------------------------------------------------
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET","POST"])
@limiter.limit(_cfg("SIGNUP_RATE","12 per minute"))
def signup():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        if not email or not password:
            flash("Please provide email and password.", "warning")
            return render_template("auth/signup.html")
        if User.query.filter_by(email=email).first():
            flash("That email is already registered.", "warning")
            return render_template("auth/signup.html")
        pwd = generate_password_hash(password)
        is_first = (User.query.count() == 0)
        user = User(email=email, password_hash=pwd, is_admin=is_first, created_at=datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        logger.info("New signup: %s", email)
        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("auth/signup.html")

@app.route("/login", methods=["GET","POST"])
@limiter.limit(_cfg("LOGIN_RATE","10 per minute"))
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.", "error")
            return render_template("auth/login.html")
        login_user(user)
        logger.info("Login: %s", email)
        return redirect(url_for("dashboard"))
    return render_template("auth/login.html")

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("login"))

# -----------------------------------------------------------------------------
# Routes: Dashboard & Transcription → Generation (SCRIPT-ONLY)
# -----------------------------------------------------------------------------
@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("main/dashboard.html")

@app.route("/transcribe", methods=["POST"])
@login_required
@limiter.limit(_cfg("TRANSCRIBE_RATE","5 per minute"))
def transcribe_route():
    product_name = (request.form.get("product_name") or "").strip()
    media_url    = (request.form.get("media_url") or "").strip()
    file         = request.files.get("media")

    if not product_name:
        flash("Please choose a product.", "warning")
        return redirect(url_for("dashboard"))

    transcript_text: Optional[str] = None
    tmp_path: Optional[str] = None

    try:
        # 1) Prefer URL if provided
        if media_url:
            transcript_text = transcribe_from_url(media_url)  # returns transcript or None
            if not transcript_text:
                path = download_from_url(media_url)  # returns local path or None
                if path:
                    transcript_text = transcribe_media(path)

        # 2) Fall back to uploaded file
        if not transcript_text and file and file.filename:
            if not _allowed_file(file.filename):
                flash("Unsupported file type.", "error")
                return redirect(url_for("dashboard"))
            fname = secure_filename(file.filename)
            tmp_dir = tempfile.mkdtemp(prefix="muse_")
            tmp_path = os.path.join(tmp_dir, fname)
            file.save(tmp_path)
            transcript_text = transcribe_media(tmp_path)

        # 3) Final fallback (keeps demo running)
        if not transcript_text:
            transcript_text = "Sample transcript (dev fallback). Install ffmpeg + faster-whisper for real transcription."

        # Auto-generate script using pretrained reviews index
        # Agent 1: analyze transcript (+ audio if available)
        try:
            media_for_analysis = tmp_path if (tmp_path and os.path.exists(tmp_path)) else None
        except Exception:
            media_for_analysis = None
        media_analysis = analyze_media(media_for_analysis, transcript_text)
        sent = media_analysis.get("sentiment", {})
        phrases_list = media_analysis.get("keywords", [])
        theme_map = {"tags": media_analysis.get("themes", [])}

        try:
            rel_reviews = ReviewIndex.search(product_name, transcript_text, k=6)
        except Exception:
            rel_reviews = []

        # Generate 10 high-quality script variations with UGC evaluation
        instagram_mode = request.form.get("instagram_mode") == "on"
        pg13_mode = request.form.get("pg13_mode") == "on"
        genz_mode = request.form.get("genz_mode") == "on"
        try:
            # Create analysis dict for generate_variations
            analysis_dict = {
                "sentiment": sent,
                "keywords": phrases_list,
                "themes": theme_map.get("tags", []),
                "hook": "",
                "style_tags": [],
                "structure": {},
                "tone": "",
                "genz_mode": genz_mode
            }
            logger.info(f"Calling generate_variations with: product={product_name}, transcript_length={len(transcript_text)}, instagram_mode={instagram_mode}, pg13_mode={pg13_mode}, genz_mode={genz_mode}")
            result = generate_variations(product_name, transcript_text, analysis_dict, rel_reviews=rel_reviews, instagram_mode=instagram_mode, pg13_mode=pg13_mode, genz_mode=genz_mode)
            logger.info(f"generate_variations result: {result}")
        except Exception as e:
            logger.error(f"Error in generate_variations: {e}")
            result = {"variations": [], "summary": "Generation failed"}
        
        generated = (result.get("variations", [{}])[0].get("text", "") or "").strip() or "No output."
        evaluation = None  # Will be calculated per variation
        variations = result.get("variations", [])
        summary = result.get("summary", "")
        logger.info(f"Final output: generated='{generated[:100]}...', variations_count={len(variations)}")

        try:
            # Save the generated script
            _save_record(current_user.id, product_name, transcript_text, generated)
        except Exception as e:
            logger.warning("Could not save record: %s", e)

        flash("Transcription and script generated successfully!", "success")
        return render_template("main/dashboard.html",
                               product_name=product_name,
                               transcript=transcript_text,
                               generated=generated,
                               evaluation=evaluation,
                               variations=variations)
    except Exception as e:
        logger.exception("Error in /transcribe: %s", e)
        flash("Something went wrong while transcribing your media.", "error")
        return render_template("main/dashboard.html")
    finally:
        # Cleanup temp file
        try:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
                os.rmdir(os.path.dirname(tmp_path))
        except Exception:
            pass

# -----------------------------------------------------------------------------
# Route: Generate from Transcript (Step 3)
# -----------------------------------------------------------------------------
@app.route("/generate", methods=["POST"])
@login_required
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
        try:
            result = generate(product_name, transcript_text, sent, phrases_list, theme_map, rel_reviews=rel_reviews, output_style=output_style)
        except TypeError:
            result = generate(product_name, transcript_text, sent, phrases_list, theme_map)
        generated = (result.get("generated") or "").strip() or "No output."

        try:
            _save_record(current_user.id, product_name, transcript_text, generated)
        except Exception as e:
            logger.warning("Could not save record: %s", e)

        flash("Script generated successfully.", "success")
        return render_template("main/dashboard.html",
                               product_name=product_name,
                               transcript=transcript_text,
                               generated=generated,
                               evaluation=result.get("evaluation"))
    except Exception as e:
        logger.exception("Error in /generate: %s", e)
        flash("Something went wrong while generating your script.", "error")
        return render_template("main/dashboard.html")

# -----------------------------------------------------------------------------
# Route: Generate 10 Variations
# -----------------------------------------------------------------------------
@app.route("/generate_variations", methods=["POST"])
@login_required
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
@login_required
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
@login_required
def admin_reviews():
    _require_admin()
    stats = ReviewIndex.stats()
    samples = ReviewIndex.samples(6)
    return render_template("admin_reviews.html", stats=stats, samples=samples)

@app.route("/admin/reviews/upload", methods=["POST"])
@login_required
def admin_reviews_upload():
    _require_admin()
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
@login_required
def admin_auto_scraper():
    _require_admin()
    
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
    return render_template("admin_auto_scraper.html", status=status)

# -----------------------------------------------------------------------------
# Route: Website Scraping
# -----------------------------------------------------------------------------
@app.route('/admin/website-scrape', methods=['GET', 'POST'])
@login_required
def admin_website_scrape():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('admin_reviews'))
    
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
    
    return render_template('admin_website_scrape.html')

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
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "true").lower() in ("1","true","yes","on")
    app.run(host=host, port=port, debug=debug)
