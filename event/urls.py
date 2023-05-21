from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('venues/', views.all_venues, name='venues'),
    path('events/', views.all_events, name='events'),
    path('add_venue/', views.add_venue, name='add-venue'),
    path('add_event/', views.add_event, name='add-event'),
    path('show_venue/<venue_id>', views.show_venue_by_id, name='show-venue'),
    path('search_venues/', views.search_for_venues, name='search-venue'),
    path('update_venue/<venue_id>', views.update_venue, name='update-venue'),
    path('delete_venue/<venue_id>', views.delete_venue, name='delete-venue'),
    path('update_event/<event_id>', views.update_event, name='update-event'),
    path('delete_event/<event_id>', views.delete_event, name='delete-event'),
    path('venue_text_download/', views.venue_text_download, name='venue-txt-dwnld'),
    path('venue_csv_download/', views.venue_csv_download, name='venue-csv-dwnld'),
    path('venue_pdf_download/', views.venue_pdf_download, name='venue-pdf-dwnld'),
    ]