from django.contrib import admin
from .models import Venue, Event
from django.contrib.auth.models import User

# admin.site.register(Venue)
# admin.site.register(Event)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'web', 'postal_code', 'email')
    ordering = ('name',)
    search_fields = ('name', 'address')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'desc', 'manager', 'visitors')
    list_display = ('name', 'event_date', 'get_visitors')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)

    def get_visitors(self, obj):
        return ", ".join([f"{every.first_name} {every.last_name}" for every in obj.visitors.all()])