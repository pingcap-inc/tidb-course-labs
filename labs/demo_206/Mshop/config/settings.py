"""
Django settings for Mshop (demo_206) - same logic as demo_205 Laravel app.
Honors Laravel-style .env names (APP_KEY, APP_DEBUG, APP_URL, URL_PREFIX, DB_*) for shared runtime.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY: APP_KEY (Laravel) or DJANGO_SECRET_KEY
_secret = os.environ.get('APP_KEY') or os.environ.get('DJANGO_SECRET_KEY')
SECRET_KEY = _secret if _secret else 'django-insecure-demo-206-change-in-production'

# DEBUG: APP_DEBUG (Laravel) or DEBUG
_debug = os.environ.get('APP_DEBUG') or os.environ.get('DEBUG')
DEBUG = str(_debug).lower() in ('1', 'true', 'yes') if _debug else True

# ALLOWED_HOSTS: derive from APP_URL host if set, else default
_app_url = os.environ.get('APP_URL', '')
if _app_url:
    from urllib.parse import urlparse
    try:
        _host = urlparse(_app_url).hostname
        ALLOWED_HOSTS = [_host] if _host else ['127.0.0.1', 'localhost']
    except Exception:
        ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
else:
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.shop_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database: DB_CONNECTION=mysql (or DB_ENGINE) and DB_* (same names as Laravel .env)
_db_engine = 'django.db.backends.mysql' if (os.environ.get('DB_CONNECTION') or os.environ.get('DB_ENGINE') or 'mysql').lower() == 'mysql' else os.environ.get('DB_ENGINE', 'django.db.backends.mysql')
DATABASES = {
    'default': {
        'ENGINE': _db_engine,
        'NAME': os.environ.get('DB_DATABASE', 'shop'),
        'USER': os.environ.get('DB_USERNAME', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Locale: APP_LOCALE (Laravel) or default
APP_LOCALE = os.environ.get('APP_LOCALE', 'en').strip().lower().replace('_', '-')
LANGUAGE_CODE = APP_LOCALE or 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'shop' / 'static'] if (BASE_DIR / 'shop' / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Optional URL prefix when behind reverse proxy (same name as Laravel .env)
URL_PREFIX = (os.environ.get('URL_PREFIX') or '').strip().rstrip('/')
if URL_PREFIX and not URL_PREFIX.startswith('/'):
    URL_PREFIX = '/' + URL_PREFIX

# Optional APP_URL for building absolute URLs (e.g. in emails or redirects)
APP_URL = os.environ.get('APP_URL', '').strip().rstrip('/')
