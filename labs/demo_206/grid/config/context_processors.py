"""
Template context: expose URL_PREFIX and app settings for reverse-proxy and links.
"""
from django.conf import settings


def grid_context(request):
    return {
        'url_prefix': getattr(settings, 'URL_PREFIX', '') or '',
        'app_name': getattr(settings, 'APP_NAME', 'grid'),
        'app_url': getattr(settings, 'APP_URL', ''),
    }
