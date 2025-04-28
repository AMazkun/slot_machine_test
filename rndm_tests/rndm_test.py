import random
import collections
import math
from scipy.stats import chisquare

def test_uniformity(generator_function, num_samples=1000000, num_bins=10):
    """
    Перевіряє рівномірність розподілу чисел, згенерованих заданою функцією.

    Args:
        generator_function: Функція, яка генерує випадкове число в діапазоні [0, 1).
        num_samples: Кількість згенерованих чисел для тестування.
        num_bins: Кількість інтервалів (бінів) для гістограми.

    Returns:
        p_value: P-значення тесту хі-квадрат. Низьке значення може свідчити про нерівномірність.
    """
    samples = [generator_function() for _ in range(num_samples)]
    bin_counts = collections.defaultdict(int)

    for sample in samples:
        bin_index = int(sample * num_bins)
        bin_counts[bin_index] += 1

    expected_count = num_samples / num_bins
    observed_counts = [bin_counts[i] for i in range(num_bins)]

    chi2, p_value = chisquare(observed_counts, f_exp=expected_count)
    return p_value

def test_mean(generator_function, num_samples=10000):
    """
    Перевіряє, чи середнє значення згенерованих чисел близьке до очікуваного (0.5 для рівномірного розподілу [0, 1)).

    Args:
        generator_function: Функція, яка генерує випадкове число в діапазоні [0, 1).
        num_samples: Кількість згенерованих чисел для тестування.

    Returns:
        mean: Середнє значення згенерованих чисел.
    """
    samples = [generator_function() for _ in range(num_samples)]
    return sum(samples) / num_samples

def test_standard_deviation(generator_function, num_samples=10000):
    """
    Перевіряє, чи стандартне відхилення згенерованих чисел близьке до очікуваного
    (приблизно 0.2887 для рівномірного розподілу [0, 1)).

    Args:
        generator_function: Функція, яка генерує випадкове число в діапазоні [0, 1).
        num_samples: Кількість згенерованих чисел для тестування.

    Returns:
        std_dev: Стандартне відхилення згенерованих чисел.
    """
    samples = [generator_function() for _ in range(num_samples)]
    mean = sum(samples) / num_samples
    variance = sum([(x - mean) ** 2 for x in samples]) / (num_samples - 1)
    return math.sqrt(variance)

if __name__ == "__main__":
    print("Тестування вбудованої функції random.random():")

    # Тест на рівномірність
    uniformity_p_value = test_uniformity(random.random)
    print(f"  P-значення тесту на рівномірність (хі-квадрат): {uniformity_p_value:.4f}")
    if uniformity_p_value > 0.05:
        print("    => Тест на рівномірність пройдено (на рівні значущості 0.05)")
    else:
        print("    => Тест на рівномірність НЕ пройдено (на рівні значущості 0.05)")

    # Тест на середнє значення
    mean_value = test_mean(random.random)
    print(f"  Середнє значення згенерованих чисел: {mean_value:.4f} (очікується ~0.5)")

    # Тест на стандартне відхилення
    std_dev_value = test_standard_deviation(random.random)
    print(f"  Стандартне відхилення згенерованих чисел: {std_dev_value:.4f} (очікується ~0.2887)")