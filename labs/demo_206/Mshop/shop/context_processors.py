from django.conf import settings


def shop_context(request):
    return {
        'url_prefix': getattr(settings, 'URL_PREFIX', '') or '',
    }
