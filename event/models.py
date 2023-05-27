from django.db import models
from django.contrib.auth.models import User


class ClubUser(models.Model):
    first_name = models.CharField('User name', max_length=100)
    last_name = models.CharField('User second name', max_length=100)
    username = models.CharField('Username', max_length=100, unique=True, null=False)
    email = models.EmailField('Email of the User')
    phone = models.CharField('User phone number', max_length=12)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=220)
    address = models.CharField(max_length=300)
    postal_code = models.CharField('Postal Code', max_length=10)
    email = models.EmailField('Email of the venue', blank=True)
    phone = models.CharField('Contacts number', max_length=12, blank=True)
    web = models.URLField('Web page', blank=True)
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    desc = models.TextField(blank=True)
    visitors = models.ManyToManyField(ClubUser, blank=True)

    def __str__(self):
        return self.name
