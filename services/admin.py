
from django.contrib import admin
from .models import Service, GalleryImage, StaffMember, QuoteRequest, Inquiry


# ... (Keep your existing ServiceAdmin, GalleryImageAdmin, etc.)

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price_start', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    search_fields = ('name', 'role')

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service_type', 'status', 'created_at')
    list_filter = ('status', 'service_type')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',) # Keeps the timestamp from being edited