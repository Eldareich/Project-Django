from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),  # Здесь 'predict' это имя маршрута
]
