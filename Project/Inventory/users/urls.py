# inventory-management-system/Project/Inventory/users/urls.py

from django.urls import path
from . import views # Import  views from the current app

app_name = 'users' #  to set an app_name for namespacing

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'), # This is the crucial line!
    path('logout/', views.logout_view, name='logout_view'),
    path('home/', views.home, name='home'),
]