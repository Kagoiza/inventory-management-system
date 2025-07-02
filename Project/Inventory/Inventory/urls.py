"""
URL configuration for Inventory project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView # <--- ADD THIS IMPORT

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirect the root URL '/' to the login page
    path('', RedirectView.as_view(pattern_name='users:login_view', permanent=False)), # <--- ADD THIS LINE FIRST
    # Include all URLs from your 'users' app under the 'users' namespace.
    # This path should come AFTER the root redirect if you want the root to always redirect.
    # If you want specific user app URLs (like /home/) to be directly accessible,
    # you might place this line before the RedirectView.
    # However, for a typical auth flow, redirecting root to login is common.
    path('', include('users.urls', namespace='users')),


    # Django's built-in authentication URLs for password reset
    # These URLs will be accessible under the 'accounts/' prefix
    path('accounts/', include('django.contrib.auth.urls')),
]

# ONLY for development: Serve static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # If you also serve media files, uncomment the line below:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
