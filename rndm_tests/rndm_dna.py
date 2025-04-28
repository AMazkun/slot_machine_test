import random
import numpy as np
from scipy.stats import chisquare

print("DNA Test begins ...")
# Генерируем случайную "ДНК-последовательность"
nucleotides = ["A", "T", "G", "C"]
sequence_length = 5000
dna_sequence = [random.choice(nucleotides) for _ in range(sequence_length)]

# Подсчет количества каждого нуклеотида
counts = {nt: dna_sequence.count(nt) for nt in nucleotides}

# Преобразуем в массив для статистического теста
observed_values = np.array(list(counts.values()))
expected_values = np.array([sequence_length / len(nucleotides)] * len(nucleotides))

# Применяем хи-квадрат тест
chi_stat, p_value = chisquare(observed_values, expected_values)

# Вывод результатов
print("Распределение нуклеотидов:", counts)
print(f"Chi-Square Statistic: {chi_stat:.2f}")
print(f"P-Value: {p_value:.4f}")

if p_value > 0.05:
    print("Гипотеза о равномерном распределении НЕ отвергается")
else:
    print("Гипотеза отвергается: последовательность НЕ случайна")
