import random
import numpy as np
from scipy.stats import chisquare

# Параметры теста
modulo = 3650  # Имитация дней в году
num_birthdays = int (modulo * 0.45)  # Количество случайных "дней рождения"

# Генерация случайных "дней рождения"
birthdays = [random.randint(0, modulo - 1) for _ in range(num_birthdays)]

# Сортируем и находим интервалы между соседними "днями рождения"
birthdays.sort()
spacings = [birthdays[i] - birthdays[i-1] for i in range(1, num_birthdays)]

# Группируем интервалы по их частоте
_, counts = np.unique(spacings, return_counts=True)

# Применяем хи-квадрат тест для проверки равномерности распределения
chi_stat, p_value = chisquare(counts)

# Вывод результатов
print(f"Chi-Square Statistic: {chi_stat:.2f}")
print(f"P-Value: {p_value:.4f}")

if p_value > 0.05:
    print("Гипотеза о равномерном распределении НЕ отвергается")
else:
    print("Гипотеза отвергается: распределение не является равномерным")
