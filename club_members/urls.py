from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.member_login, name='member-login'),
    path('logout/', views.member_logout, name='member-logout'),
    path('register/', views.register_user, name='register-user'),
]