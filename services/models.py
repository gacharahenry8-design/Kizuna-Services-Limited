from django.db import models
from django.db import models


class QuoteRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    service_type = models.CharField(max_length=100, default='General Cleaning')
    date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service_type}"


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('Residential', 'Residential Cleaning'),
        ('Commercial', 'Commercial Cleaning'),
        ('Specialty', 'Specialty Cleaning'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    price_start = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon_class = models.CharField(max_length=50, help_text="FontAwesome class, e.g., fas fa-spray-can-sparkles")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # ← ADD THIS
    category = models.CharField(max_length=50, choices=[('Residential', 'Residential'), ('Commercial', 'Commercial')])
    created_at = models.DateTimeField(auto_now_add=True)

    def get_image_url(self):
        if self.image and self.image.name:
            return self.image.url
        if self.image_url:
            return self.image_url
        return ''

    def __str__(self):
        return self.title

class StaffMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='staff/', blank=True, null=True)

    def __str__(self):
        return self.name


class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    youtube_id = models.CharField(max_length=20, help_text="Just the ID, e.g. dQw4w9WgXcQ")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class ContactMessage(models.Model):
    SERVICE_CHOICES = [
        ("general", "General Cleaning"),
        ("deep", "Deep Cleaning"),
        ("office", "Office Cleaning"),
        ("carpet", "Specialized Carpet Care"),
        ("post-construction", "Post-Construction Cleaning"),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=150)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} – {self.service} ({self.submitted_at.date()})"

class CareerApplication(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Reviewed', 'Reviewed'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
    ]
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    position = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    cover_letter = models.TextField()
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} – {self.position} ({self.submitted_at.date()})"
