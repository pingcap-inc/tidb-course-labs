"""
URL configuration for Mshop - same routes as demo_205 Laravel web.php.
"""
from django.urls import path, include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', include('shop.urls')),
]
if getattr(settings, 'DEBUG', False):
    from pathlib import Path
    media_assets = Path(settings.BASE_DIR) / 'media' / 'assets'
    if media_assets.exists():
        urlpatterns += [path('assets/<path:path>', serve, {'document_root': media_assets})]
