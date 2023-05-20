from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.all_events, name='events'),
    path('add_venue/', views.add_venue, name='add-venue'),
    path('venues/', views.all_venues, name='venues'),
    path('show_venue/<venue_id>', views.show_venue_by_id, name='show-venue'),
    path('search_venues/', views.search_for_venues, name='search-venue'),
    path('update_venue/<venue_id>', views.update_venue, name='update-venue'),
    path('add_event/', views.add_event, name='add-event'),
    ]