# views.py — clean imports (replace the scattered duplicates at the top)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import QuoteForm, BookingForm, CareerApplicationForm
from .models import QuoteRequest, Service, GalleryImage, StaffMember, Video, ContactMessage, CareerApplication


# --- ACCESS CONTROL ---

def admin_only(user):
    return user.is_staff


# --- PUBLIC VIEWS ---

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
    staff_members = StaffMember.objects.all()
    return render(request, 'about.html', {'staff': staff_members})

def gallery(request):
    images = GalleryImage.objects.all().order_by('-created_at')
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'gallery.html', {'images': images, 'videos': videos})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage


def contact_view(request):
    """
    Handles the Contact Us page.
    - GET:  Renders the contact form.
    - POST: Validates and saves the submitted form to the database,
            then redirects back with a success message.
    """
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email     = request.POST.get("email", "").strip()
        phone     = request.POST.get("phone", "").strip()
        location  = request.POST.get("location", "").strip()
        service   = request.POST.get("service", "").strip()
        message   = request.POST.get("message", "").strip()

        # --- Server-side validation ---
        errors = []
        if not full_name:
            errors.append("Full name is required.")
        if not email or "@" not in email:
            errors.append("A valid email address is required.")
        if not phone:
            errors.append("Phone number is required.")
        if not location:
            errors.append("Location is required.")
        if not service:
            errors.append("Please select a service.")
        if not message:
            errors.append("Message cannot be empty.")

        if errors:
            for error in errors:
                messages.error(request, error)
            # Re-render with user's input preserved
            return render(request, "contact.html", {
                "form_data": {
                    "full_name": full_name,
                    "email":     email,
                    "phone":     phone,
                    "location":  location,
                    "service":   service,
                    "message":   message,
                }
            })

        # --- Save to database ---
        ContactMessage.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            location=location,
            service=service,
            message=message,
        )

        messages.success(
            request,
            "Thank you! Your message has been received. We'll be in touch shortly."
        )
        return redirect("contact")

    return render(request, "contact.html")
    contact = contact_view  # ← this line is unreachable and does nothing, delete it



def career(request):
    if request.method == 'POST':
        # Pass request.FILES to handle the uploaded CV file
        form = CareerApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            # 1. Extract cleaned data from the form
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            position = form.cleaned_data['position']
            experience = form.cleaned_data['experience']
            cover_letter = form.cleaned_data['cover_letter']
            cv_file = form.cleaned_data['cv']  # This holds the uploaded file

            # 2. Handle or Save the Data
            # Option A: If you created an Applicant model, save it directly:
            # Applicant.objects.create(
            #     full_name=full_name, email=email, phone_number=phone_number,
            #     position=position, experience=experience, cover_letter=cover_letter, cv=cv_file
            # )

            CareerApplication.objects.create(
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                position=position,
                experience=experience,
                cover_letter=cover_letter,
                cv=cv_file,
            )

            # 3. Trigger a success banner to display on the page
            messages.success(request, "Your application has been submitted successfully! We will get back to you soon.")

            # Redirect back to the career page to prevent duplicate submissions on refresh
            return redirect('career')
        else:
            messages.error(request, "There was an error in your submission. Please check the fields below.")
    else:
        # It's a GET request, load an empty instance of the form
        form = CareerApplicationForm()

    context = {
        'form': form
    }
    return render(request, 'career.html', context)

def book(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your booking has been submitted!")
            return redirect('book')
        else:
            print("Form errors:", form.errors)
            messages.error(request, f"Form error: {form.errors}")
    else:
        form = BookingForm()

    return render(request, 'book.html', {'form': form})


# --- ADMIN DASHBOARD VIEWS (protected) ---

@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def admin_dashboard(request):
    return redirect('inquiries_list')


@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def inquiries_list(request):
    pending = QuoteRequest.objects.filter(status='Pending').order_by('-created_at')
    completed = QuoteRequest.objects.filter(status='Completed').order_by('-created_at')
    return render(request, 'dashboard/inquiries.html', {
        'pending': pending,
        'completed': completed,
        'inquiries': QuoteRequest.objects.all().order_by('-created_at'),
    })


# --- SERVICE MANAGEMENT ---

@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def services_manage(request):
    services_list = Service.objects.all()
    return render(request, 'dashboard/services_manage.html', {'services': services_list})


@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def add_service(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        icon = request.POST.get('icon', 'fas fa-sparkles')

        Service.objects.create(
            title=title,
            description=description,
            price_start=price,
            category=category,
            icon_class=icon
        )

        messages.success(request, f"Service '{title}' has been added successfully!")
        return redirect('services_manage')

    return render(request, 'dashboard/services.html')


@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
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


@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.delete()
        messages.success(request, "Service deleted permanently.")
        return redirect('services_manage')
    return render(request, 'dashboard/delete_confirm.html', {'service': service})


# --- GALLERY MANAGEMENT ---

@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def gallery_manage(request):
    images = GalleryImage.objects.all().order_by('-created_at')
    videos = Video.objects.all().order_by('-created_at')
    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        image_file = request.FILES.get('image_file')
        image_url = request.POST.get('image_url')

        if image_file:
            GalleryImage.objects.create(title=title, image=image_file, category=category)
            messages.success(request, "Image uploaded successfully!")
        elif image_url:
            GalleryImage.objects.create(title=title, image_url=image_url, category=category)
            messages.success(request, "Image added via link!")
        else:
            messages.error(request, "Please provide an image file or a link.")

        return redirect('gallery_manage')
    return render(request, 'dashboard/gallery.html', {'images': images, 'videos': videos})

@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def delete_gallery_image(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)
    if request.method == "POST":
        image.delete()
        messages.success(request, "Image removed from gallery.")
    return redirect('gallery_manage')


# --- STAFF MANAGEMENT ---

@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def staff_manage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        role = request.POST.get('role')
        bio = request.POST.get('bio')
        image = request.FILES.get('image')

        StaffMember.objects.create(name=name, role=role, bio=bio, image=image)
        messages.success(request, "New team member added!")
        return redirect('staff_manage')

    staff_list = StaffMember.objects.all()
    return render(request, 'dashboard/staff.html', {'staff': staff_list})


@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def delete_staff(request, pk):
    person = get_object_or_404(StaffMember, pk=pk)
    if request.method == "POST":
        person.delete()
        messages.success(request, f"Staff member '{person.name}' removed successfully.")
    return redirect('staff_manage')


@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
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


# --- INQUIRY MANAGEMENT ---

@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
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


@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def mark_complete(request, pk):
    inquiry = get_object_or_404(QuoteRequest, pk=pk)
    if request.method == 'POST':
        inquiry.status = 'Completed'
        inquiry.save()
        messages.success(request, f"{inquiry.name}'s inquiry marked as complete.")
    return redirect('inquiries_list')

@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def video_manage(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        youtube_id = request.POST.get('youtube_id')
        Video.objects.create(title=title, description=description, youtube_id=youtube_id)
        messages.success(request, "Video added successfully!")
        return redirect('gallery_manage')  # ← redirect to gallery, not video_manage
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'dashboard/gallery.html', {'videos': videos})  # ← gallery.html

@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == "POST":
        video.delete()
        messages.success(request, "Video removed.")
    return redirect('video_manage')

# --- CAREER APPLICATIONS DASHBOARD ---

@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def applications_list(request):
    applications = CareerApplication.objects.all().order_by('-submitted_at')
    return render(request, 'dashboard/applications.html', {'applications': applications})


@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def update_application_status(request, pk):
    application = get_object_or_404(CareerApplication, pk=pk)
    if request.method == 'POST':
        application.status = request.POST.get('status')
        application.save()
        messages.success(request, f"Status updated to '{application.status}' for {application.full_name}.")
    return redirect('applications_list')


@login_required(login_url='/login/')
@user_passes_test(admin_only, login_url='/login/')
def delete_application(request, pk):
    application = get_object_or_404(CareerApplication, pk=pk)
    if request.method == 'POST':
        application.delete()
        messages.success(request, "Application deleted.")
    return redirect('applications_list')
