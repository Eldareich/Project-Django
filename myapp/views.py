from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

# Страница регистрации
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизация сразу после регистрации
            return redirect('home')  # Перенаправление на главную
    else:
        form = RegisterForm()
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
