from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.http import HttpResponse

urlpatterns = [
    # Main Website Pages
    path('', views.home, name='home'),
    path('home/', RedirectView.as_view(url='/', permanent=False)),  # fix /home/ 404
    path('favicon.ico', lambda request: HttpResponse(status=204)),  # silence favicon 404
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact_view, name='contact'),
    path('career/', views.career, name='career'),
    path('book/', views.book, name='book'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),  # ← keep only one

    # Custom Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/inquiries/', views.inquiries_list, name='inquiries_list'),
    path('dashboard/inquiries/reply/<int:pk>/', views.reply_inquiry, name='reply_inquiry'),
    path('dashboard/inquiries/complete/<int:pk>/', views.mark_complete, name='mark_complete'),
    path('dashboard/services/', views.services_manage, name='services_manage'),
    path('dashboard/services/add/', views.add_service, name='add_service'),
    path('dashboard/services/edit/<int:pk>/', views.edit_service, name='edit_service'),
    path('dashboard/services/delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('dashboard/gallery/', views.gallery_manage, name='gallery_manage'),
    path('dashboard/gallery/delete/<int:pk>/', views.delete_gallery_image, name='delete_gallery_image'),
    path('dashboard/videos/', views.video_manage, name='video_manage'),
    path('dashboard/videos/delete/<int:pk>/', views.delete_video, name='delete_video'),
    path('dashboard/staff/', views.staff_manage, name='staff_manage'),
    path('dashboard/staff/delete/<int:pk>/', views.delete_staff, name='delete_staff'),
    path('dashboard/staff/edit/<int:pk>/', views.edit_staff, name='edit_staff'),
    path('dashboard/applications/', views.applications_list, name='applications_list'),
    path('dashboard/applications/status/<int:pk>/', views.update_application_status, name='update_application_status'),
    path('dashboard/applications/delete/<int:pk>/', views.delete_application, name='delete_application'),
]