# extensions.py — central place to create Flask extension singletons
from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Database
db = SQLAlchemy()

# Auth/session
login_manager = LoginManager()

# CSRF protection (what app.py imports as `csrf`)
csrf = CSRFProtect()

# Rate limiting (app.py imports as `limiter`)
# We don’t set default limits here; app.py supplies them via init_app.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],    # let app.py configure defaults
    storage_uri=None,     # in-memory for dev; set Redis URI for prod
)

__all__ = ["db", "login_manager", "csrf", "limiter"]
