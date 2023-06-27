from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from datetime import datetime


def member_login(request):

    if request.method == "POST":
        username = request.POST['Username']
        # email = request.POST['InputEmail']
        password = request.POST['Password']
        # phone_number = request.POST['InputPhone']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('calendar_specific', year=datetime.now().year, month=datetime.now().strftime("%B"))
        else:
            messages.success(request, "There was an error while logging. Try again.")
            return redirect('member-login')

    elif request.method == "GET":
        return render(request, 'authentication/login.html', {})


def member_logout(request):
    logout(request)
    messages.success(request, "You were successfully logged out")
    return redirect('calendar_specific')


def register_user(request):
    date = datetime.datetime.now().date()
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect('calendar_specific', year=date.year, month=date.month)
    else:
        form = RegisterUserForm()

    return render(request, 'authentication/registration.html', {"form": form})
