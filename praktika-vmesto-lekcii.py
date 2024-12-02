# Заданий №1
import requests

# 1.1 Отправка GET-запроса к API GitHub
response = requests.get("https://api.github.com/search/repositories", params={"q": "html"})
print("Статус-код:", response.status_code)  # Статус-код ответа
print("Содержимое ответа в формате JSON:", response.json())  # JSON-ответ

# 1.2 Отправка GET-запроса с параметром userId
response = requests.get("https://jsonplaceholder.typicode.com/posts", params={"userId": 1})
print("Статус-код:", response.status_code)  # Статус-код ответа
print("Полученные записи:", response.json())  # JSON-ответ

# Данные для отправки
post_data = {"title": "foo", "body": "bar", "userId": 1}
# 1.3 Отправка POST-запроса
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=post_data)
print("Статус-код:", response.status_code)  # Статус-код ответа
print("Ответ сервера:", response.json())  # JSON-ответ

# Задание №2: Поиск на Википедии
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Настройка браузера
browser = webdriver.Chrome()

# Спрашиваем у пользователя начальный запрос
query = input("Введите запрос для поиска на Википедии: ")

# Переход на главную страницу Википедии
browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")
assert "Википедия" in browser.title
time.sleep(2)

# Поиск запроса
search_box = browser.find_element(By.ID, "searchInput")
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)
time.sleep(3)

while True:
    print("Выберите действие:")
    print("1. Листать параграфы статьи")
    print("2. Перейти на связанную страницу")
    print("3. Выйти")
    choice = input("Введите номер действия: ")

    if choice == "1":
        # Листание параграфов
        paragraphs = browser.find_elements(By.TAG_NAME, "p")
        for paragraph in paragraphs:
            print(paragraph.text)
            input("Нажмите Enter для продолжения...")
    elif choice == "2":
        # Переход на связанную страницу
        links = browser.find_elements(By.TAG_NAME, "a")
        print("Связанные страницы:")
        for idx, link in enumerate(links[:10]):  # Показываем первые 10 ссылок
            print(f"{idx + 1}. {link.text or 'Без названия'}")
        selected = int(input("Выберите номер ссылки: ")) - 1
        links[selected].click()
        time.sleep(3)
    elif choice == "3":
        print("Выход из программы.")
        break
    else:
        print("Неверный выбор. Попробуйте снова.")

browser.quit()
