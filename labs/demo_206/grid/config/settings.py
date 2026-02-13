"""
Django settings for demo_206 grid app.
Reads from runtime .env (loaded in manage.py / wsgi / asgi): APP_*, URL_PREFIX, DB_*, etc.
URL_PREFIX is used when running behind a reverse proxy (e.g. /vscode/proxy/8000).
"""
import os
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent

# --- App / Laravel-style .env names ---
APP_NAME = os.environ.get('APP_NAME', 'grid')
APP_ENV = os.environ.get('APP_ENV', 'local')
APP_KEY = os.environ.get('APP_KEY') or os.environ.get('DJANGO_SECRET_KEY')
SECRET_KEY = (APP_KEY or 'django-insecure-demo-206-change-in-production').strip()

_debug = os.environ.get('APP_DEBUG') or os.environ.get('DEBUG')
DEBUG = str(_debug).lower() in ('1', 'true', 'yes') if _debug is not None else True

APP_URL = (os.environ.get('APP_URL') or '').strip().rstrip('/')

# URL_PREFIX: required when behind reverse proxy (e.g. /vscode/proxy/8000)
_url_prefix = (os.environ.get('URL_PREFIX') or '').strip().rstrip('/')
if _url_prefix and not _url_prefix.startswith('/'):
    _url_prefix = '/' + _url_prefix
URL_PREFIX = _url_prefix

# FORCE_SCRIPT_NAME so Django generates correct URLs behind proxy (redirects, {% url %}, static)
if URL_PREFIX:
    FORCE_SCRIPT_NAME = URL_PREFIX
else:
    FORCE_SCRIPT_NAME = None

# ALLOWED_HOSTS: from APP_URL host or explicit list
#if APP_URL:
#    try:
#        _host = urlparse(APP_URL).hostname
#        ALLOWED_HOSTS = [_host] if _host else ['127.0.0.1', 'localhost']
#    except Exception:
#        ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
#else:
#    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

ALLOWED_HOSTS = ['*']

# --- i18n: en, ja, zh ---
APP_LOCALE = (os.environ.get('APP_LOCALE') or 'en').strip().lower().replace('_', '-')
# Map to Django language codes (zh -> zh-hans for Simplified Chinese)
_locale_map = {'en': 'en', 'ja': 'ja', 'zh': 'zh-hans', 'zh-hans': 'zh-hans', 'zh-cn': 'zh-hans'}
LANGUAGE_CODE = _locale_map.get(APP_LOCALE.split('-')[0], 'en')

LANGUAGES = [
    ('en', 'English'),
    ('ja', '日本語'),
    ('zh-hans', '中文'),
]
LOCALE_PATHS = [BASE_DIR / 'grid' / 'locale']

# --- Apps & middleware ---
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grid',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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
                'django.template.context_processors.static',
                'django.template.context_processors.i18n',
                'config.context_processors.grid_context',
            ],
        },
    },
]
WSGI_APPLICATION = 'config.wsgi.application'

# --- Database (DB_CONNECTION=pgsql/postgresql, DB_*) ---
_db_conn = (os.environ.get('DB_CONNECTION') or 'pgsql').lower()
if _db_conn in ('pgsql', 'postgres', 'postgresql'):
    _db_engine = 'django.db.backends.postgresql'
else:
    _db_engine = os.environ.get('DB_ENGINE', 'django.db.backends.postgresql')

DATABASES = {
    'default': {
        'ENGINE': _db_engine,
        'NAME': os.environ.get('DB_DATABASE', 'grid_db'),
        'USER': os.environ.get('DB_USERNAME', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static: respect URL_PREFIX so assets load correctly behind proxy
if URL_PREFIX:
    STATIC_URL = URL_PREFIX.rstrip('/') + '/static/'
else:
    STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'grid' / 'static'] if (BASE_DIR / 'grid' / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
