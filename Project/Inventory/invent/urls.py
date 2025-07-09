from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register, name='register'),
    path('custom_login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Requestor Paths
    path('', views.requestor_dashboard, name='requestor_dashboard'),
    path('request_item/', views.request_item, name='request_item'),
    path('search-items/', views.search_items, name='search_items'),

    # Store Clerk Paths
    path('store_clerk_dashboard/', views.store_clerk_dashboard, name ='store_clerk_dashboard'),
    path('manage_stock/', views.manage_stock, name = 'manage_stock'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    
    # NEW Functionalities (Issue and Adjust)
    path('issue_item/', views.issue_item, name='issue_item'),
    path('adjust_stock/', views.adjust_stock, name='adjust_stock'),
]