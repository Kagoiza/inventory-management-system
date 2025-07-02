from django.urls import path
from . import views # Import your custom views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'), # Use your custom login_view
    path('logout/', views.logout_view, name='logout'), # Add logout URL
    path('home/', views.home, name='home'), # Add home URL
    path('requestor_dashboard/', views.requestor_dashboard, name='requestor-dashboard'),
]

