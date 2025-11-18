"""
Django settings for feedback project (production-ready)

Adapted for production:
 - Uses environment variables for secrets and flags
 - Enforces SECRET_KEY existence (fail-fast)
 - Secure cookie / HTTPS / HSTS settings
 - Staticfile & media settings suitable for collectstatic
 - Basic logging for production
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

# Base dir & env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

def get_env_variable(name: str) -> str:
    """Return the environment variable or raise ImproperlyConfigured."""
    value = os.getenv(name)
    if not value:
        raise ImproperlyConfigured(f"Set the {name} environment variable")
    return value

# SECURITY
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')

# Debug flag controlled via env; default False in production
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('1', 'true', 'yes')

# Allowed hosts - comma separated list in env (example: "example.com,www.example.com")
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',') if h.strip()]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'feedback_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise serves static files efficiently in production
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'feedback.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'feedback.wsgi.application'


# Database — unchanged, environment-driven MySQL config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'feedback_db'),
        'USER': os.getenv('MYSQL_USER', 'YOUR_DB_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
        'HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.getenv('MYSQL_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': int(os.getenv('CONN_MAX_AGE', '60')),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Kathmandu')
USE_I18N = True
USE_TZ = True


# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']            # dev static sources
STATIC_ROOT = BASE_DIR / 'staticfiles'              # collectstatic target (production)

# If you use WhiteNoise (recommended for simple deployments), enable it in MIDDLEWARE above
# Use WhiteNoise for static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media (uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Security-related settings (enabled if DEBUG is False)
if not DEBUG:
    # Must use HTTPS in production; control via env var to allow testing on non-HTTPS hosts if needed
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() in ('1','true','yes')
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() in ('1','true','yes')
    CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True').lower() in ('1','true','yes')
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True').lower() in ('1','true','yes')
    SECURE_HSTS_PRELOAD = os.getenv('SECURE_HSTS_PRELOAD', 'True').lower() in ('1','true','yes')
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

    # If your app is behind a proxy (e.g., nginx), set this:
    # SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    proxy_ssl_header = os.getenv('SECURE_PROXY_SSL_HEADER', '')
    if proxy_ssl_header:
        # expected format: "HTTP_X_FORWARDED_PROTO,https"
        try:
            header, value = proxy_ssl_header.split(',', 1)
            SECURE_PROXY_SSL_HEADER = (header.strip(), value.strip())
        except ValueError:
            # ignore malformed value
            pass

    # Trust specific origins for CSRF (comma separated)
    cs_roots = [u.strip() for u in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if u.strip()]
    if cs_roots:
        CSRF_TRUSTED_ORIGINS = cs_roots

# Admins / managers
ADMINS = tuple(os.getenv('ADMINS', '').split(',')) if os.getenv('ADMINS') else ()
MANAGERS = ADMINS


# Logging — simple production logging to console (adapt to file/Sentry as needed)
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'}
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'standard'}
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
    'loggers': {
        'django.db.backends': {'level': 'ERROR', 'handlers': ['console'], 'propagate': False},
    }
}