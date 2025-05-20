from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),                         # Админка Django
    path('', include('cvapp.urls')),                         # Основной функционал (резюме и шаблоны)
    path('salary/', include('SalaryPredictionApp.urls')),    # Модуль прогнозов зарплат
    path('accounts/', include('accounts.urls')),             # Регистрация / логин / аккаунты
]

# Подключаем обработку медиафайлов (для изображений шаблонов и профилей)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
