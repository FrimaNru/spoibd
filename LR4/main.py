import random
import numpy as np
import secrets
import matplotlib.pyplot as plt

# Реализация методов генерации случайных чисел

# Метод 1: random.randint()
def my_rand1(n):
    return [random.randint(1, 6) for _ in range(n)]

# Метод 2: random.choice()
def my_rand2(n):
    return [random.choice([1, 2, 3, 4, 5, 6]) for _ in range(n)]

# Метод 3: numpy.random.randint()
def my_rand3(n):
    return np.random.randint(1, 7, n)

# Метод 4: secrets.randbelow()
def my_rand4(n):
    return [secrets.randbelow(6) + 1 for _ in range(n)]

# Функция для генерации бросков кубика
def generate_rolls(method, n):
    if method == 1:
        return my_rand1(n)
    elif method == 2:
        return my_rand2(n)
    elif method == 3:
        return my_rand3(n)
    elif method == 4:
        return my_rand4(n)

# Размеры выборок
sizes = [100, 1000, 10000, 1000000]
colors = ['blue', 'green', 'orange', 'purple']

# Словарь для хранения данных
data = {1: {}, 2: {}, 3: {}, 4: {}}

# Генерация данных
for size in sizes:
    for method in range(1, 5):
        data[method][size] = generate_rolls(method, size)

# Построение гистограмм
fig, axes = plt.subplots(4, 4, figsize=(20, 15))  # 4x4 сетка для каждого метода и размера

for i, method in enumerate(range(1, 5)):
    for j, size in enumerate(sizes):
        axes[i, j].hist(data[method][size], bins=6, color=colors[j], alpha=0.7)
        axes[i, j].set_title(f'Метод {method}, {size} бросков')
        axes[i, j].set_xlabel('Результат броска')
        axes[i, j].set_ylabel('Количество')

plt.tight_layout()
plt.show()

# Проверка данных
# Построим распределение для каждого метода и размера выборки, чтобы убедиться в корректности
for method in range(1, 5):
    print(f"Метод {method}")
    for size in sizes:
        rolls = data[method][size]
        
        # Если rolls — это numpy.ndarray, используем np.bincount()
        if isinstance(rolls, np.ndarray):
            counts = np.bincount(rolls, minlength=7)[1:7]  # бинкаунт возвращает от 0 до 6, берем с 1 до 6
        else:
            counts = [rolls.count(i) for i in range(1, 7)]
        
        distribution = {i + 1: counts[i] / len(rolls) for i in range(6)}
        print(f"{size} бросков: {distribution}")
    print("\n")