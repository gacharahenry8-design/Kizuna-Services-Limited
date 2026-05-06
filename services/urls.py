from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Make sure this import is here

urlpatterns = [
    # Main Website Pages
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),

    # Custom Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/inquiries/', views.inquiries_list, name='inquiries_list'),
    path('dashboard/services/', views.services_manage, name='services_manage'),
    path('dashboard/inquiries/reply/<int:pk>/', views.reply_inquiry, name='reply_inquiry'),
    path('dashboard/inquiries/complete/<int:pk>/', views.mark_complete, name='mark_complete'),
    path('dashboard/services/add/', views.add_service, name='add_service'),
    path('dashboard/services/edit/<int:pk>/', views.edit_service, name='edit_service'),
    path('dashboard/services/delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('dashboard/gallery/', views.gallery_manage, name='gallery_manage'),
    path('dashboard/gallery/delete/<int:pk>/', views.delete_gallery_image, name='delete_gallery_image'),
    path('dashboard/staff/', views.staff_manage, name='staff_manage'),
    path('dashboard/staff/delete/<int:pk>/', views.delete_staff, name='delete_staff'),
    path('dashboard/staff/edit/<int:pk>/', views.edit_staff, name='edit_staff'),
    path('book/', views.book, name='book'),
    # Logout path
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]