from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *

# Create your views here.


def index(request):
    return render(request, "user/user.html")


def user_signup(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')
    else:
        form = UserCreateForm()
    return render(request, 'user/signup.html', {"form": form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home:home')
            else:
                messages.error(request, "아이디와 비밀번호가 일치하지 않거나 존재하지 않습니다.")
        else:
            messages.error(request, "아이디와 비밀번호가 일치하지 않거나 존재하지 않습니다.")
            print("Form Errors: ", form.errors)
            print("Non-field Errors: ", form.non_field_errors())
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home:home')
