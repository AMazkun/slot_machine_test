import numpy as np
import random
from scipy.linalg import lu

print("Matrix Rank Test begins ...")

# Параметры теста
matrix_size = 32  # Размер квадратной матрицы
num_matrices = 1000  # Количество случайных матриц


# Функция генерации случайных матриц и проверки ранга
def matrix_rank_test(matrix_size, num_matrices):
    full_rank_count = 0

    for _ in range(num_matrices):
        # Создаем случайную бинарную матрицу (0 или 1)
        matrix = np.random.randint(0, 2, (matrix_size, matrix_size))

        # Проверяем ранг матрицы
        rank = np.linalg.matrix_rank(matrix)

        if rank == matrix_size:
            full_rank_count += 1

    # Оцениваем вероятность полного ранга
    rank_ratio = full_rank_count / num_matrices

    print(f"Матриц с полным рангом: {full_rank_count} из {num_matrices}")
    print(f"Вероятность полного ранга: {rank_ratio:.4f}")

    if rank_ratio > 0.95:
        print("Генератор проходит Matrix Rank Test!")
    else:
        print("Есть подозрение на отклонение от случайности.")


# Запуск теста
matrix_rank_test(matrix_size, num_matrices)
