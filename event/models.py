from django.db import models
from django.contrib.auth.models import User


class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=220)
    address = models.CharField(max_length=300)
    postal_code = models.CharField('Postal Code', max_length=10)
    email = models.EmailField('Email of the venue', blank=True)
    phone = models.CharField('Contacts number', max_length=12, blank=True)
    web = models.URLField('Web page', blank=True)
    desc = models.TextField(blank=True)
    owner = models.IntegerField("Venue Owner", blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='manager')
    desc = models.TextField(blank=True)
    visitors = models.ManyToManyField(User, blank=True)
    approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.name
