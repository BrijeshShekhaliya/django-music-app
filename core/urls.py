# core/urls.py

from django.contrib import admin
from django.urls import path, include # Make sure to import include
from django.conf import settings # New import
from django.conf.urls.static import static # New import

urlpatterns = [
    path('admin/', admin.site.urls),
    # Add this line to include your music app's URLs
    path('', include('music.urls')), 
    # Add this line to include django-allauth's URLs
    path('accounts/', include('allauth.urls')),
]

# Add this line to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)