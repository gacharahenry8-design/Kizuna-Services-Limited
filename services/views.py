from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import QuoteForm, BookingForm
from .models import QuoteRequest, Service, GalleryImage, StaffMember

def home(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your quote request has been sent successfully!")
            return redirect('home')
    else:
        form = QuoteForm()

    return render(request, 'home.html', {'form': form})

def services(request):
    services_list = Service.objects.all()
    return render(request, 'services.html', {'services': services_list})

def about(request):
    # Fetch all staff members from the database
    staff_members = StaffMember.objects.all()
    return render(request, 'about.html', {'staff': staff_members})

def gallery(request):
    images = GalleryImage.objects.all().order_by('-created_at')
    return render(request, 'gallery.html', {'images': images})


# --- ADMIN DASHBOARD OVERVIEW ---

def admin_dashboard(request):
    return redirect('inquiries_list')

def inquiries_list(request):
    pending = QuoteRequest.objects.filter(status='Pending').order_by('-created_at')
    completed = QuoteRequest.objects.filter(status='Completed').order_by('-created_at')
    return render(request, 'dashboard/inquiries.html', {
        'pending': pending,
        'completed': completed,
        'inquiries': QuoteRequest.objects.all().order_by('-created_at')  # keep for any other use
    })

def services_manage(request):
    # Fetch from database
    services_list = Service.objects.all()

    # THE FIX: The key 'services' must match the {% for service in services %}
    return render(request, 'dashboard/services_manage.html', {'services': services_list})


def add_service(request):
    if request.method == "POST":
        # Capture data from the form
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        icon = request.POST.get('icon', 'fas fa-sparkles')  # Default if empty

        # Save to database
        Service.objects.create(
            title=title,
            description=description,
            price_start=price,
            category=category,
            icon_class=icon
        )

        messages.success(request, f"Service '{title}' has been added successfully!")
        return redirect('services_manage')

    # This view usually won't be hit via GET if you are using the toggle form,
    # but it's good to have as a fallback.
    return render(request, 'dashboard/services.html')


def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.title = request.POST.get('title')
        service.description = request.POST.get('description')
        service.price_start = request.POST.get('price')
        service.save()
        messages.success(request, "Service updated successfully!")
        return redirect('services_manage')
    return render(request, 'dashboard/edit_service.html', {'service': service})

def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.delete()
        messages.success(request, "Service deleted permanently.")
        return redirect('services_manage')
    return render(request, 'dashboard/delete_confirm.html', {'service': service})


# --- GALLERY MANAGEMENT ---

def gallery_manage(request):
    images = GalleryImage.objects.all().order_by('-created_at')
    if request.method == "POST":
        image_file = request.FILES.get('image_file')
        title = request.POST.get('title')
        category = request.POST.get('category')  # Add this line

        if image_file:
            # Add category=category here
            GalleryImage.objects.create(title=title, image=image_file, category=category)
            messages.success(request, "Image uploaded to gallery!")
            return redirect('gallery_manage')
    return render(request, 'dashboard/gallery.html', {'images': images})

def delete_gallery_image(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)
    if request.method == "POST":
        image.delete()
        messages.success(request, "Image removed from gallery.")
    return redirect('gallery_manage')


def staff_manage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        role = request.POST.get('role')
        bio = request.POST.get('bio')
        image = request.FILES.get('image')

        StaffMember.objects.create(
            name=name,
            role=role,
            bio=bio,
            image=image
        )
        messages.success(request, "New team member added!")
        return redirect('staff_manage')

    staff_list = StaffMember.objects.all()
    return render(request, 'dashboard/staff.html', {'staff': staff_list})

def delete_staff(request, pk):
    person = get_object_or_404(StaffMember, pk=pk)
    if request.method == "POST":
        person.delete()
        messages.success(request, f"Staff member '{person.name}' removed successfully.")
    return redirect('staff_manage')

def edit_staff(request, pk):
    person = get_object_or_404(StaffMember, pk=pk)
    if request.method == "POST":
        person.name = request.POST.get('name')
        person.role = request.POST.get('role')
        person.bio = request.POST.get('bio')
        
        if request.FILES.get('image'):
            person.image = request.FILES.get('image')
            
        person.save()
        messages.success(request, f"Updated {person.name} successfully!")
        return redirect('staff_manage')
    
    return render(request, 'dashboard/edit_staff.html', {'person': person})

def book(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your booking has been submitted!")
            return redirect('book')
        else:
            # ADD THIS — print errors to console or pass to template
            print("Form errors:", form.errors)  # Check your terminal
            messages.error(request, f"Form error: {form.errors}")  # Show in browser
    else:
        form = BookingForm()

    return render(request, 'book.html', {'form': form})


def reply_inquiry(request, pk):
    inquiry = get_object_or_404(QuoteRequest, pk=pk)
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [inquiry.email],
            fail_silently=False,
        )
        messages.success(request, f"Reply sent to {inquiry.email}!")
        return redirect('inquiries_list')
    return render(request, 'dashboard/reply_inquiry.html', {'inquiry': inquiry})

def mark_complete(request, pk):
    inquiry = get_object_or_404(QuoteRequest, pk=pk)
    if request.method == 'POST':
        inquiry.status = 'Completed'
        inquiry.save()
        messages.success(request, f"{inquiry.name}'s inquiry marked as complete.")
    return redirect('inquiries_list')