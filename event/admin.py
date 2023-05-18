from django.contrib import admin
from .models import Venue, ClubUser, Event

# admin.site.register(Venue)
admin.site.register(ClubUser)
# admin.site.register(Event)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'desc', 'manager')
    list_display = ('name', 'event_date')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)