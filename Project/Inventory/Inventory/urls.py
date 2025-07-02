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
    path('register/', user_views.register, name='register'),
    # Using your custom login_view from users.views
    path('login/', user_views.login_view, name='login'),
    # Adding the logout view from users.views
    path('logout/', user_views.logout_view, name='logout'),
    # Correcting the home view reference to use user_views
    path('home/', user_views.home, name='home'),
    path('', user_views.requestor_dashboard, name='requestor_dashboard'),
]

# ONLY for development: Serve static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # If you also serve media files, uncomment the line below:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
