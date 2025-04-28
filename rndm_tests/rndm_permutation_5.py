import random
import numpy as np
from collections import Counter

print("Permutation 5 Overlapping Test begins ...")

# Генерируем последовательность случайных чисел
size = 1000000  # Длина последовательности
sequence = [random.randint(0, 255) for _ in range(size)]  # Числа от 0 до 255

# Формируем 5-пермутационные последовательности (с перекрытием)
five_permutations = [tuple(sequence[i:i+5]) for i in range(size - 4)]  # Генерируем группы из 5 чисел

# Считаем частоту появления каждой уникальной 5-пермутации
counts = Counter(five_permutations)

# Анализируем частоту появления уникальных значений
unique_count = len(counts)  # Количество уникальных 5-элементных групп
expected_count = (256**5)  # Ожидаемое количество уникальных комбинаций (если случайно)

# Оцениваем случайность
randomness_ratio = unique_count / expected_count

# Вывод результатов
print(f"Уникальных 5-пермутаций: {unique_count}")
print(f"Ожидаемое количество (теоретически): {expected_count}")
print(f"Отношение уникальности: {randomness_ratio:.6f}")

if randomness_ratio > 0.95:
    print("Генератор случайных чисел проходит тест!")
else:
    print("Есть подозрение на отклонение от случайности!")
