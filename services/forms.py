from django import forms
from .models import QuoteRequest

class QuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        # Ensure 'website' is in this list if you want it on the form
        fields = ['name', 'email', 'phone', 'website', 'service_type', 'message']