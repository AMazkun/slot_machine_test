import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Параметры теста
num_points = 500  # Количество случайных точек
dimension = 3  # Трехмерное пространство

# Генерация случайных точек в 3D-пространстве
points = np.array([[random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)] for _ in range(num_points)])

# Вычисление всех парных расстояний
distances = []
for i in range(num_points):
    for j in range(i + 1, num_points):
        dist = np.linalg.norm(points[i] - points[j])  # Евклидово расстояние
        distances.append(dist)

# Определяем минимальное расстояние
min_distance = min(distances)

# Вывод результатов
print(f"Минимальное расстояние между точками: {min_distance:.4f}")

# Визуализация точек в 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:, 0], points[:, 1], points[:, 2], alpha=0.5)
ax.set_title(f"Minimum Distance Test (мин. расстояние = {min_distance:.4f})")
plt.show()
