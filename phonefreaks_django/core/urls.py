from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('phone/<str:phone_id>/', views.phone_detail, name='phone_detail'),
    path('compare/', views.compare, name='compare'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('register/', views.register_view, name='register'),
    path('user-login/', views.login_view, name='user_login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin URLs
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('custom-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('custom-admin/add/', views.admin_add_phone, name='admin_add_phone'),
    path('custom-admin/edit/<str:phone_id>/', views.admin_edit_phone, name='admin_edit_phone'),
    path('custom-admin/delete/<str:phone_id>/', views.admin_delete_phone, name='admin_delete_phone'),
    path('custom-admin/users/', views.manage_users, name='manage_users'),
    path('custom-admin/users/toggle/<int:user_id>/', views.toggle_admin_role, name='toggle_admin_role'),
]
