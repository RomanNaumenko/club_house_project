import io
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import ClubUser, Venue, Event
from .forms import VenueForm, EventForm
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
import csv
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.exceptions import PermissionDenied
from django.contrib import messages


# Create your views here.
def home(request):

    username = None
    superuser_events = None
    user_events = None

    if request.user.is_superuser:
        superuser_events = Event.objects.all().order_by("event_date")
    if request.user.is_authenticated:

        username = request.user.get_username()
        user_by_username = ClubUser.objects.filter(username=username).first()
        if user_by_username:
            user_id = user_by_username.id
            user_events = Event.objects.filter(visitors__id=user_id)

    return render(request, 'events/home.html', {"name": username, "superuser_events": superuser_events,
                                                "user_events": user_events})


def all_events(request):
    events = Event.objects.all().order_by('-event_date', 'venue')
    return render(request, 'events/events.html', {"events": events})


def all_venues(request):
    # venues = Venue.objects.all().order_by('?')
    # venues = Venue.objects.all().order_by('name')
    pagy = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = pagy.get_page(page)
    nums = "a" * venues.paginator.num_pages
    return render(request, 'events/venues.html', {"venues": venues, 'nums': nums})


def add_venue(request):
    if request.user.is_superuser:

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
    else:

        messages.success(request, "Before you will be able to add venues, you must log in first.")
        return redirect('member-login')


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
    if request.user.is_superuser:

        venue = Venue.objects.get(pk=venue_id)
        form = VenueForm(request.POST or None, instance=venue)
        if form.is_valid():
            form.save()
            return redirect('venues')
        return render(request, 'events/update_venue.html', {"venue": venue, 'form': form})
    else:

        messages.success(request, "Before you will be able to add venues, you must log in first.")
        return redirect('member-login')


def add_event(request):
    if request.user.is_superuser:

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
    else:

        messages.success(request, "Before you will be able to add venues, you must log in first.")
        return redirect('member-login')


def update_event(request, event_id):
    if request.user.is_superuser:

        event = Event.objects.get(pk=event_id)
        form = EventForm(request.POST or None, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events')
        return render(request, 'events/update_event.html', {"event": event, 'form': form})
    else:

        messages.success(request, "Before you will be able to add venues, you must log in first.")
        return redirect('member-login')


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('events')


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('venues')


def venue_text_download(request):
    date = datetime.datetime.now().date()
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=venues_list_{date}.txt'
    venues = Venue.objects.all()

    for venue in venues:
        venue_lines = [f"Venue name: {venue.name}\n",
                       f"Venue address: {venue.address}\n",
                       f"Venue postal_code: {venue.postal_code}\n",
                       f"Venue email: {venue.email}\n",
                       f"Venue phone: {venue.phone}\n",
                       f"Venue web: {venue.web}\n",
                       f"Venue desc: {venue.desc}\n\n\n"]

        response.writelines(venue_lines)
    return response


def venue_csv_download(request):
    date = datetime.datetime.now().date()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=venues_list_{date}.csv'
    venues = Venue.objects.all()

    rows = [['Venue Name', 'Address', 'ZIP Code', 'Email', 'Phone', 'Web', 'Description']]
    for venue in venues:
        rows.append([venue.name, venue.address, venue.postal_code, venue.email,
                     venue.phone, venue.web, venue.desc])

    writer = csv.writer(response)
    writer.writerows(rows)
    return response


def venue_pdf_download(request):
    date = datetime.datetime.now().date()
    #  Create Bytestream buffer
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #  Create Test Object
    text_object = c.beginText()
    text_object.setTextOrigin(inch, inch)
    text_object.setFont("Helvetica", 14)

    #  Add some lines
    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        lines.append(f"Venue name: {venue.name}")
        lines.append(f"Venue address: {venue.address}")
        lines.append(f"Venue postal_code: {venue.postal_code}")
        lines.append(f"Venue email: {venue.email}")
        lines.append(f"Venue phone: {venue.phone}")
        lines.append(f"Venue web: {venue.web}")
        lines.append(f"Venue desc: {venue.desc}")
        lines.append("_______________________________________________")
        lines.append(" ")
        lines.append(" ")

    for line in lines:
        text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename=f'venue_list_{date}.pdf')
