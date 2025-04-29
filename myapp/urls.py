# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('home/', views.resume_form, name='home'),
    path('result/', views.resume_result, name='result'),
    path('login/', views.login_view, name='login'),
    
]
