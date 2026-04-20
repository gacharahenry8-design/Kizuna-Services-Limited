from django import forms
from .models import QuoteRequest

class QuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['name', 'email', 'website', 'message']