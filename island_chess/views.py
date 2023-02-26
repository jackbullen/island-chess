from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password, backend='django.contrib.auth.backends.ModelBackend')
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def board_view(request):
    return render(request, 'board/board.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password2')
            user = authenticate(username=username, password=raw_password, backend='django.contrib.auth.backends.ModelBackend')
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_view(request):
    return render(request, 'profile.html')

def settings_view(request):
    return render(request, 'settings.html')