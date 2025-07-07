from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register, name='register'),
    path('custom_login', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.requestor_dashboard, name='requestor_dashboard'),
    path('request_item', views.request_item, name='request_item'),
    path('store_clerk_dashboard', views.store_clerk_dashboard, name ='store_clerk_dashboard'),
    path('manage_stock', views.manage_stock, name = 'manage_stock'),
]