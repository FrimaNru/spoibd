from Levenshtein import distance as levenshtein_distance
from Levenshtein import ratio as levenshtein_ratio
from fuzzywuzzy import fuzz
import time

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

# Функции для сравнения строк
def compare_levenshtein(str1, str2):
    start = time.time()
    dist = levenshtein_distance(str1, str2)
    ratio = levenshtein_ratio(str1, str2)
    end = time.time()
    return dist, ratio, end - start

def compare_fuzzywuzzy(str1, str2):
    start = time.time()
    ratio = fuzz.ratio(str1, str2)
    partial_ratio = fuzz.partial_ratio(str1, str2)
    token_sort = fuzz.token_sort_ratio(str1, str2)
    token_set = fuzz.token_set_ratio(str1, str2)
    end = time.time()
    return ratio, partial_ratio, token_sort, token_set, end - start

def levenshtein_manual(s1, s2):
    start = time.time()
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

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
    dist = dp[len_s1][len_s2]
    ratio = 1 - dist / max(len_s1, len_s2)
    end = time.time()
    return dist, ratio, end - start

# Автоматическое тестирование
results = []
for case in test_cases:
    str1, str2 = case
    lev_result = compare_levenshtein(str1, str2)
    fuzzy_result = compare_fuzzywuzzy(str1, str2)
    manual_result = levenshtein_manual(str1, str2)

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
