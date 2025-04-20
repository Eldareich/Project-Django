from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume_form, name='home'),             
    path('preview/', views.resume_result, name='preview'),
     path('register/', views.register, name='register'),
]
