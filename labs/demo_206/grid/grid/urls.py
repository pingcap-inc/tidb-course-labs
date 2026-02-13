from django.urls import path
from .views import GridView

urlpatterns = [
    path('', GridView.as_view(), name='grid'),
]
