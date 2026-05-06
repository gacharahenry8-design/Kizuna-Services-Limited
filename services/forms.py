from django import forms
from .models import QuoteRequest

class QuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['name', 'email', 'phone', 'website', 'service_type', 'message']
        # Matches exactly what's in your home.html form

class BookingForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['name', 'email', 'phone', 'service_type', 'date', 'location', 'message']
        # Adjust to match what's in your book.html form