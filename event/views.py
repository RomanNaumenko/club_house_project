import io
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Venue, Event
from .forms import VenueForm, RegularUserEventForm, SuperUserEventForm
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
import csv
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib import messages
import calendar
from calendar import HTMLCalendar
from datetime import datetime


# Create your views here.
def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):

    name = request.user.username
    if request.user.is_anonymous:
        name = None
    month = month.capitalize()
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar
    cal = HTMLCalendar().formatmonth(
        year,
        month_number)
    # Get current year
    now = datetime.now()
    current_year = now.year

    # Query the Events Model For Dates
    event_list = Event.objects.filter(
        event_date__year=year,
        event_date__month=month_number
    )

    # Get current time
    time = now.strftime('%I:%M %p')
    return render(request,
                  'events/home.html', {
                      "name": name,
                      "year": year,
                      "month": month,
                      "month_number": month_number,
                      "cal": cal,
                      "current_year": current_year,
                      "time": time,
                      "event_list": event_list,
                  })


def all_events(request):
    events = Event.objects.all().order_by('-event_date', 'venue')
    return render(request, 'events/events.html', {"events": events})


def all_venues(request):
    # venues = Venue.objects.all().order_by('?')
    # venues = Venue.objects.all().order_by('name')
    pagy = Paginator(Venue.objects.all(), 4)
    page = request.GET.get('page')
    venues = pagy.get_page(page)
    nums = "a" * venues.paginator.num_pages
    return render(request, 'events/venues.html', {"venues": venues, 'nums': nums})


def add_venue(request):
    if request.user.is_superuser:

        submitted = False
        if request.method == "POST":
            form = VenueForm(request.POST, request.FILES)
            if form.is_valid():
                venue = form.save(commit=False)
                venue.owner = request.user.id
                venue.save()
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
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html', {"venue": venue, "venue_owner": venue_owner})


def search_for_venues(request):
    if request.method == "POST":
        searcher = request.POST.get("searcher", False)
        venues = Venue.objects.filter(name__contains=searcher)
        return render(request, 'events/search_for_venues.html',
                      {'searcher': searcher, 'venues': venues})
    else:
        return render(request, 'events/search_for_venues.html',
                      {})


def search_for_events(request):
    if request.method == "POST":
        searcher = request.POST.get("searcher", False)

        if searcher:
            events = Event.objects.filter(name__contains=searcher)
        else:
            events = Event.objects.all().order_by('-event_date', 'venue')

        return render(request, 'events/events.html',
                      {'searcher': searcher, 'events': events})
    else:
        return render(request, 'events/events.html',
                      {})


def update_venue(request, venue_id):
    if request.user.is_authenticated:

        venue = Venue.objects.get(pk=venue_id)
        form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
        if form.is_valid():
            form.save()
            return redirect('venues')
        return render(request, 'events/update_venue.html', {"venue": venue, 'form': form})

    else:

        messages.success(request, "Before you will be able to add venues, you must log in first.")
        return redirect('member-login')


def add_event(request):
    if request.user.is_authenticated:

        submitted = False
        if request.method == "POST":
            if request.user.is_superuser:
                form = SuperUserEventForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/home/add_event?submitted=True')
            else:
                form = RegularUserEventForm(request.POST)

                if form.is_valid():
                    event = form.save(commit=False)
                    event.manager = request.user
                    event.save()
                    return HttpResponseRedirect('/home/add_event?submitted=True')
        if request.user.is_superuser:
            form = SuperUserEventForm
        else:
            form = RegularUserEventForm
        if 'submitted' in request.GET:
            submitted = True
        return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted, 'user': request.user})
    else:

        messages.success(request, "Before you will be able to add venues, you must log in first.")
        return redirect('member-login')


def update_event(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(pk=event_id)
        if request.user.is_superuser:
            form = SuperUserEventForm(request.POST or None, instance=event)
        else:
            form = RegularUserEventForm(request.POST or None, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events')
        return render(request, 'events/update_event.html', {"event": event, 'form': form, 'user': request.user})
    else:

        messages.success(request, "Before you will be able to add venues, you must log in first.")
        return redirect('member-login')


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, "Event deleted.")
        return redirect('events')
    else:
        messages.success(request, "No permission for such action.")
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


def my_events(request):
    if request.user.is_authenticated:
        my_events = Event.objects.filter(visitors=request.user.id)
        return render(request, 'events/my_events.html', {"events": my_events, "user": request.user})
    else:
        messages.success(request, "You have not proper authorization to access this page!")
        return redirect('home')
