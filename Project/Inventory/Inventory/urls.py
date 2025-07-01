"""
URL configuration for Inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from users import views as user_views # Correct import for your users app views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    # Using your custom login_view from users.views
    path('login/', user_views.login_view, name='login'),
    # Adding the logout view from users.views
    path('logout/', user_views.logout_view, name='logout'),
    # Correcting the home view reference to use user_views
    path('', user_views.home, name='home'),
]

# ONLY for development: Serve static files
# This block should only be used during development (DEBUG=True)
# For production, static files are typically served by a web server (e.g., Nginx, Apache)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # If you also serve media files, uncomment the line below:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
