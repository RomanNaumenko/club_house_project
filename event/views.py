from django.shortcuts import render
from .models import ClubUser, Venue, Event
from .forms import VenueForm
from django.http import HttpResponseRedirect


# Create your views here.
def home(request):
    return render(request, 'events/home.html', {"name": "Roman"})


def all_events(request):
    events = Event.objects.all()
    return render(request, 'events/events.html', {"events": events})


def all_venues(request):
    venues = Venue.objects.all()
    return render(request, 'events/venues.html', {"venues": venues})


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home/add_venue?submitted=True')
    form = VenueForm
    if 'submitted' in request.GET:
        submitted = True
    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


def show_venue_by_id(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'events/show_venue.html', {"venue": venue})
