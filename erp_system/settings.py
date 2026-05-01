import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
DEBUG = env_bool("DEBUG", False)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".vercel.app",
    ".railway.app",
    ".up.railway.app",
    "2400030008.pythonanywhere.com",
]

extra_hosts = os.environ.get("ALLOWED_HOSTS", "")
if extra_hosts:
    ALLOWED_HOSTS.extend(host.strip() for host in extra_hosts.split(",") if host.strip())

CSRF_TRUSTED_ORIGINS = [
    "https://*.vercel.app",
    "https://*.railway.app",
    "https://*.up.railway.app",
]

extra_csrf = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if extra_csrf:
    CSRF_TRUSTED_ORIGINS.extend(origin.strip() for origin in extra_csrf.split(",") if origin.strip())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users.apps.UsersConfig",
    "students",
    "attendance",
    "grades",
    "timetable",
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

ROOT_URLCONF = "erp_system.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "students.context_processors.sidebar_students",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
            ],
        },
    }
]

WSGI_APPLICATION = "erp_system.wsgi.application"

IS_RAILWAY = bool(
    os.environ.get("RAILWAY_ENVIRONMENT")
    or os.environ.get("RAILWAY_PROJECT_ID")
    or os.environ.get("RAILWAY_SERVICE_ID")
)
IS_VERCEL = bool(os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV"))


def postgres_config_from_url(database_url):
    db_url = urlparse(database_url)
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": db_url.path.lstrip("/"),
        "USER": db_url.username,
        "PASSWORD": db_url.password,
        "HOST": db_url.hostname,
        "PORT": db_url.port or "5432",
        "CONN_MAX_AGE": 600,
    }


DATABASE_URL = (
    os.environ.get("DATABASE_URL")
    or os.environ.get("DATABASE_PRIVATE_URL")
    or os.environ.get("DATABASE_PUBLIC_URL")
)

if DATABASE_URL:
    DATABASES = {"default": postgres_config_from_url(DATABASE_URL)}
elif os.environ.get("PGHOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("PGDATABASE", "railway"),
            "USER": os.environ.get("PGUSER", "postgres"),
            "PASSWORD": os.environ.get("PGPASSWORD", ""),
            "HOST": os.environ.get("PGHOST"),
            "PORT": os.environ.get("PGPORT", "5432"),
            "CONN_MAX_AGE": 600,
        }
    }
elif os.environ.get("POSTGRES_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "ERP"),
            "USER": os.environ.get("POSTGRES_USER", "postgres"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
            "CONN_MAX_AGE": 600,
        }
    }
elif IS_RAILWAY:
    raise ImproperlyConfigured(
        "Railway deployment needs a PostgreSQL variable. Add DATABASE_URL from "
        "your Railway PostgreSQL service, or link the PostgreSQL service so PGHOST, "
        "PGDATABASE, PGUSER, and PGPASSWORD are available."
    )
elif env_bool("USE_SQLITE", True):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.CustomUser"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"

if IS_VERCEL:
    SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
