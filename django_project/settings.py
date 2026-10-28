"""
Django settings for the Scarlet Roasters case-company app — 33:136:440.

The public pages keep the Week 5 setup. The operations app maps the existing
class PostgreSQL database for the Week 7 Admin and Status pages.
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Vercel's environment wins; local settings can come from either lab file name.
load_dotenv(BASE_DIR / ".env.local", override=False)
load_dotenv(BASE_DIR / ".env", override=False)

# WEEK 5 — secrets stay out of the repository.
# Locally the fallback is used. On Vercel, set SECRET_KEY in Project → Settings → Environment Variables.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "dev-only-not-secret-change-me-in-production-8f2k1",
)

# WEEK 5 — DEBUG is on on your laptop and off on Vercel (Vercel sets the VERCEL variable).
DEBUG = "VERCEL" not in os.environ

# WEEK 5 — who may serve this site.
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".vercel.app"]
CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pages",  # WEEK 5 — our app
    "operations.apps.OperationsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # WEEK 5 — project-level templates (base.html lives here)
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_project.wsgi.application"  # Vercel reads this line to find the app

# DATABASE_URL must point to the existing, seeded class database on Neon.
# Without it, /status/ reports the missing PostgreSQL setup and 0 of 11 tables.
database_url = os.environ.get("DATABASE_URL", "").strip()
if database_url:
    database = dj_database_url.parse(
        database_url,
        conn_max_age=0,
        ssl_require="VERCEL" in os.environ,
    )
    if database["ENGINE"] == "django.db.backends.postgresql":
        database.setdefault("OPTIONS", {})["connect_timeout"] = 10
        database["DISABLE_SERVER_SIDE_CURSORS"] = True
else:
    database = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:" if "VERCEL" in os.environ else BASE_DIR / "db.sqlite3",
    }
DATABASES = {"default": database}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True

# WEEK 5 — static files. STATIC_ROOT is what makes Vercel run collectstatic and serve /static/ from its CDN.
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
