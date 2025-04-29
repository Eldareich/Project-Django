from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def login_view(request):
    return render(request, 'myapp/login.html')

@login_required
def resume_form(request):
    days = range(1, 32)
    years = range(1950, 2026)
    return render(request, 'myapp/home.html', {'days': days, 'years': years})

@login_required
def resume_result(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        education = request.POST.get('education')
        experience = request.POST.get('experience')
        return render(request, 'myapp/result.html', {
            'name': name,
            'education': education,
            'experience': experience,
        })
    return render(request, 'myapp/home.html')
