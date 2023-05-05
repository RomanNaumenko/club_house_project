from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_specific, name='calendar_specific'),
    path('<int:year>/<str:month>/', views.calendar_specific, name='calendar_specific'),
    ]