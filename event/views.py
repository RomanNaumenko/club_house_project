from django.shortcuts import render
from .models import User, Venue, Event


# Create your views here.
def home(request):
    return render(request, 'events/home.html', {"name": "Roman"})


def all_events(request):
    events = Event.objects.all()
    return render(request, 'events/events.html', {"events": events})
