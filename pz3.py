from Levenshtein import distance as levenshtein_distance
from Levenshtein import ratio as levenshtein_ratio
from fuzzywuzzy import fuzz
import time

# Задачи из статьи:
# 1. Вычисление расстояния Левенштейна (задача "Расстояние между строками").
# 2. Вычисление коэффициента схожести строк (задача "Сравнение строк").
# 3. Использование различных подходов для сравнения строк (задача "Оптимизация метода сравнения").
# 4. Сравнение производительности разных методов.

# Примеры строк для тестирования
test_cases = [
    ("машинное обучение", "обучение машинное"),
    ("привет мир", "мир привет"),
    ("Python programming", "Python programming language"),
    ("искусственный интеллект", "искуственный интелект"),  # Опечатка
    ("data science", "data scientist"),
    ("hello world", "world hello"),
    ("случайное совпадение", "случайное"),
    ("12345", "123456"),
    ("example string", "sample string"),
    ("математика", "математический анализ"),
]

# Функция для сравнения строк с использованием python-Levenshtein
def compare_levenshtein(str1, str2):
    """
    Сравнивает строки с использованием библиотеки python-Levenshtein.
    Возвращает расстояние Левенштейна, коэффициент схожести и время выполнения.
    Задача: "Расстояние между строками" и "Сравнение строк".
    """
    start = time.time()
    dist = levenshtein_distance(str1, str2)  # Расстояние Левенштейна
    ratio = levenshtein_ratio(str1, str2)  # Коэффициент схожести
    end = time.time()
    return dist, ratio, end - start

# Функция для сравнения строк с использованием библиотеки fuzzywuzzy
def compare_fuzzywuzzy(str1, str2):
    """
    Сравнивает строки с использованием библиотеки fuzzywuzzy.
    Возвращает коэффициенты схожести (общий, частичный, с сортировкой и с учетом набора) и время выполнения.
    Задача: "Оптимизация метода сравнения".
    """
    start = time.time()
    ratio = fuzz.ratio(str1, str2)  # Общий коэффициент схожести
    partial_ratio = fuzz.partial_ratio(str1, str2)  # Частичный коэффициент
    token_sort = fuzz.token_sort_ratio(str1, str2)  # С учетом сортировки
    token_set = fuzz.token_set_ratio(str1, str2)  # С учетом множества
    end = time.time()
    return ratio, partial_ratio, token_sort, token_set, end - start

# Функция для ручного вычисления расстояния Левенштейна
def levenshtein_manual(s1, s2):
    """
    Реализация алгоритма Левенштейна вручную.
    Возвращает расстояние Левенштейна, коэффициент схожести и время выполнения.
    Задача: "Расстояние между строками".
    """
    start = time.time()
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]  # Матрица расстояний

    # Заполнение матрицы расстояний
    for i in range(len_s1 + 1):
        for j in range(len_s2 + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    dist = dp[len_s1][len_s2]  # Расстояние Левенштейна
    ratio = 1 - dist / max(len_s1, len_s2)  # Коэффициент схожести
    end = time.time()
    return dist, ratio, end - start

# Автоматическое тестирование всех методов
results = []
for case in test_cases:
    str1, str2 = case
    lev_result = compare_levenshtein(str1, str2)  # Метод python-Levenshtein
    fuzzy_result = compare_fuzzywuzzy(str1, str2)  # Метод fuzzywuzzy
    manual_result = levenshtein_manual(str1, str2)  # Ручной метод

    results.append({
        "Strings": (str1, str2),
        "Levenshtein": lev_result,
        "FuzzyWuzzy": fuzzy_result,
        "Manual Levenshtein": manual_result
    })

# Вывод результатов
for res in results:
    print(f"Сравнение строк: {res['Strings']}")
    print(f"  Levenshtein (dist, ratio, time): {res['Levenshtein']}")
    print(f"  FuzzyWuzzy (ratio, partial, token_sort, token_set, time): {res['FuzzyWuzzy']}")
    print(f"  Manual Levenshtein (dist, ratio, time): {res['Manual Levenshtein']}")
    print("-" * 80)
