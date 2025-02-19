import telebot
import threading
import random
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Настройки Flask и SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://047084354_zvir:Arti2005@mysql.j1007852.myjino.ru:3306/j1007852_237_zvir"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Создание объекта бота
bot = telebot.TeleBot("8178279080:AAFGRlo8wjW16NIkAyp0DAUT8RvdyvTExxg")

# Модель Fact для базы данных
class Fact(db.Model):
    __tablename__ = 'facts'
    id = db.Column(db.String(36), primary_key=True)
    text = db.Column(db.String(50), nullable=False)

# Словарь случайных приветствий
random_phrases = {
    1: "Привет! Хорошо, что ты здесь!",
    2: "Добро пожаловать! Давай вместе следить за водным балансом!",
    3: "Привет! Не забывай пить воду, чтобы быть в форме!",
}

# Переменная для контроля потока
stop_sending_facts = False

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    random_start_msg = random.choice(list(random_phrases.values()))
    bot.reply_to(message, random_start_msg)

# Функция для отправки случайного факта из базы данных
def send_random_fact_from_db(chat_id):
    global stop_sending_facts
    with app.app_context():  # Создаем контекст приложения
        while not stop_sending_facts:  # Проверка флага
            try:
                facts = Fact.query.all()  # Получаем все факты из базы данных
                if not facts:
                    bot.send_message(chat_id, "В базе данных пока нет фактов.")
                    break

                random_fact = random.choice(facts).text  # Выбираем случайный факт
                bot.send_message(chat_id, f'Интересный факт: {random_fact}')
                time.sleep(10)  # Задержка между отправками
            except Exception as e:
                print(f"Ошибка при работе с базой данных: {e}")
                break

# Команда /facts
@bot.message_handler(commands=['facts'])
def facts_message(message):
    global stop_sending_facts
    stop_sending_facts = False  # Сбрасываем флаг, чтобы начать отправку фактов
    chat_id = message.chat.id
    threading.Thread(target=send_random_fact_from_db, args=(chat_id,)).start()
    bot.reply_to(message, 'Я начну присылать тебе интересные факты каждые 10 секунд! Напиши /stop для того чтобы остановить')

# Команда /stop - остановка отправки фактов
@bot.message_handler(commands=['stop'])
def stop_message(message):
    global stop_sending_facts
    stop_sending_facts = True  # Устанавливаем флаг для остановки отправки фактов
    bot.reply_to(message, "Я больше не буду присылать факты.")

# Команда /game
@bot.message_handler(commands=['game'])
def start_game(message):
    bot.reply_to(message, 'Игра началась! Напиши слово "стоп", чтобы закончить игру.')

# Обработка сообщений для игры
@bot.message_handler(func=lambda message: True)
def game_message(message):
    if message.text.lower() == "стоп":
        bot.reply_to(message, "Игра окончена! Спасибо за участие.")
    else:
        response = random.choice(["Ты угадал!", "Попробуй снова!", "Интересная попытка!"])
        bot.reply_to(message, response)

# Функция запуска Flask-приложения
def run_app():
    app.run(debug=True, use_reloader=False)

# Функция запуска бота
def run_bot():
    bot.polling(none_stop=True)

# Запуск приложения и бота
if __name__ == "__main__":
    threading.Thread(target=run_app).start()  # Запуск Flask
    run_bot()  # Запуск бота
