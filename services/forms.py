from django import forms
from .models import QuoteRequest

class QuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['name', 'email', 'phone', 'website', 'service_type', 'message']
        # Matches exactly what's in your home.html form

class BookingForm(forms.ModelForm):
    message = forms.CharField(required=False, widget=forms.Textarea)
    class Meta:
        model = QuoteRequest
        fields = ['name', 'email', 'phone', 'service_type', 'date', 'location', 'message']


from django import forms


class CareerApplicationForm(forms.Form):
    POSITION_CHOICES = [
        ('supervisor', 'Cleaning Supervisor'),
        ('cleaner', 'Office Cleaner'),
        ('technician', 'Carpet Cleaning Technician'),
        ('intern', 'Internship Opportunity'),
    ]

    full_name = forms.CharField(max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    position = forms.ChoiceField(choices=POSITION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    experience = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of Experience'}))
    cover_letter = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us why you are a great fit...'}))
    cv = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))