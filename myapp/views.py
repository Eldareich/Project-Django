from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm

# Страница регистрации
def register(request):
    # Если пользователь уже авторизован, перенаправляем на главную страницу
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя
            login(request, user)  # Авторизуем пользователя сразу после регистрации
            return redirect('home')  # Перенаправляем на главную страницу
    else:
        form = RegisterForm()  # Инициализируем пустую форму

    return render(request, 'myapp/register.html', {'form': form})

# Главная страница для авторизованных пользователей
@login_required
def resume_form(request):
    return render(request, 'myapp/home.html')

# Страница с результатами для авторизованных пользователей
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
