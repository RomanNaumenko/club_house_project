from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def member_login(request):
    if request.method == "POST":
        username = request.POST['Username']
        # email = request.POST['InputEmail']
        password = request.POST['Password']
        # phone_number = request.POST['InputPhone']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "There was an error while logging. Try again.")
            return redirect('member-login')

    elif request.method == "GET":
        return render(request, 'authentication/login.html', {})
