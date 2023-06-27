from django import forms
from django.forms import ModelForm
from .models import Venue, Event
# from datetimepicker.widgets import DateTimePicker


class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'phone', 'email', 'web', 'desc', 'postal_code')
        labels = {
            'name': '',
            'address': '',
            'phone': '',
            'email': '',
            'web': '',
            'description': '',
            'postal_code': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Webpage'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code'})
        }


class SuperUserEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager', 'desc', 'visitors')
        labels = {
            'name': '',
            'event_date': '',
            'venue': 'Venue',
            'manager': 'Manager',
            'description': 'Description',
            'visitors': 'Visitors',

        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'DD.MM.YYYY'},
                format='%Y-%m-%dT%H:%M'
            ),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'visitors': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Visitors'})
        }


class RegularUserEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'desc', 'visitors')
        labels = {
            'name': '',
            'event_date': '',
            'venue': 'Venue',
            'description': 'Description',
            'visitors': 'Visitors',

        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'DD.MM.YYYY'},
                format='%Y-%m-%dT%H:%M'
            ),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'visitors': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Visitors'})
        }