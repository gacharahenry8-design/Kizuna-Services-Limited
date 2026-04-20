from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import QuoteForm  # Make sure you've created forms.py


def home(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            # This adds a success message that you can display in your HTML
            messages.success(request, "Your quote request has been sent successfully!")
            return redirect('home')
    else:
        form = QuoteForm()

    return render(request, 'home.html', {'form': form})


def services(request):
    return render(request, 'services.html')

def about(request):
    return render(request, 'about.html')

def gallery(request):
    return render(request, 'gallery.html')
