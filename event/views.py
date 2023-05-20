from django.shortcuts import render, redirect
from .models import ClubUser, Venue, Event
from .forms import VenueForm, EventForm
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


def search_for_venues(request):
    if request.method == "POST":
        searcher = request.POST.get("searcher", False)
        venues = Venue.objects.filter(name__contains=searcher)
        return render(request, 'events/search_for_venues.html',
                      {'searcher': searcher, 'venues': venues})
    else:
        return render(request, 'events/search_for_venues.html',
                      {})


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('venues')
    return render(request, 'events/update_venue.html', {"venue": venue, 'form': form})


def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home/add_event?submitted=True')
    form = EventForm
    if 'submitted' in request.GET:
        submitted = True
    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('events')
    return render(request, 'events/update_event.html', {"event": event, 'form': form})


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('events')


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('venues')
