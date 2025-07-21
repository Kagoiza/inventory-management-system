from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register, name='register'),
    path('custom_login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Requestor Paths
    path('', views.requestor_dashboard, name='requestor_dashboard'),
    path('request_item/', views.request_item, name='request_item'),
    path('request_summary/', views.request_summary, name='request_summary'),
    path('cancel-request/<int:request_id>/',
         views.cancel_request, name='cancel_request'),


    # Store Clerk Paths
    path('store_clerk_dashboard/', views.store_clerk_dashboard,
         name='store_clerk_dashboard'),
    path('manage_stock/', views.manage_stock, name='manage_stock'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('reports/', views.reports_view, name='reports'),

    # NEW Functionalities (Issue and Adjust)

    path('issue-item/', views.issue_item, name='issue_item'),
    path('adjust_stock/', views.adjust_stock, name='adjust_stock'),
    path('upload-inventory/', views.upload_inventory, name='upload_inventory'),

    # Reports
    path('reports/total-requests/', views.total_requests, name='total_requests'),
    path('reports/export/total-requests/', views.export_total_requests, name='export_total_requests'),



]
