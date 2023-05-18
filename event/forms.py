from django import forms
from django.forms import ModelForm
from .models import Venue, ClubUser, Event


class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'phone', 'email', 'web')
        labels = {
            'name': '',
            'address': '',
            'phone': '',
            'email': '',
            'web': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Webpage'})
        }
