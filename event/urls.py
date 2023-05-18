from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.all_events, name='events'),
    path('add_venue/', views.add_venue, name='add-venue'),
    path('venues/', views.all_venues, name='venues'),
    path('show_venue/<venue_id>', views.show_venue_by_id, name='show-venue'),
    ]