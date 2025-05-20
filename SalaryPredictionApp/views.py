from django.shortcuts import render
from sklearn.linear_model import LinearRegression  # Импортируем модель линейной регрессии
from django.http import HttpResponse
import numpy as np


def predict(request):
    # Обработка POST-запроса
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            experience = float(request.POST.get('experience'))

            # Пример данных для обучения модели
            experience_data = np.array([[1], [2], [3], [4], [5]])  # 1-5 лет опыта
            salary_data = np.array([30000, 40000, 50000, 60000, 70000])  # Примерные зарплаты

            # Создаем модель линейной регрессии
            model = LinearRegression()
            model.fit(experience_data, salary_data)

            # Предсказываем зарплату по введенному опыту
            predicted_salary = model.predict(np.array([[experience]]))[0]

            # Возвращаем результат на страницу
            return render(request, 'SalaryPredictionApp/predict.html', {'prediction': round(predicted_salary, 2)})

        except ValueError:
            # Если введены некорректные данные
            return render(request, 'SalaryPredictionApp/predict.html', {'error': 'Please enter a valid number.'})

    # Обработка GET-запроса, если пользователь просто открыл страницу
    return render(request, 'SalaryPredictionApp/predict.html')
