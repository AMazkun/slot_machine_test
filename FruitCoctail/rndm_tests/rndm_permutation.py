import random
import numpy as np
from scipy.stats import permutation_test

print("Permutation Test begins ...")

# Генерация двух выборок случайных чисел
size = 50000
random_numbers_1 = [random.random() for _ in range(size)]
random_numbers_2 = [random.random() for _ in range(size)]  # Вторая выборка

# Функция для вычисления различий между выборками
def statistic(x, y):
    return abs(np.mean(x) - np.mean(y))

# Проведение пермутационного теста
result = permutation_test((random_numbers_1, random_numbers_2), statistic, n_resamples=10000, alternative='two-sided')

# Вывод результатов
print(f"P-Value: {result.pvalue:.4f}")
if result.pvalue > 0.05:
    print("Гипотеза о случайности НЕ отвергается.")
else:
    print("Гипотеза отвергается: данные могут быть неслучайными.")
