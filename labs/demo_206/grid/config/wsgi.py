"""
WSGI config for grid project.
"""
import os
from pathlib import Path

# Load runtime .env from project root before Django reads settings
_env_path = Path(__file__).resolve().parent.parent / '.env'
if _env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(_env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
