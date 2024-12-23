from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import main  # Импорт блюпринта после инициализации db
    app.register_blueprint(main)

    with app.app_context():
        from app import models  # Импорт моделей внутри контекста приложения

    return app

# Функция для загрузки пользователя по ID
@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Перемещаем импорт User сюда, чтобы избежать циклической зависимости
    return User.query.get(user_id)
