from flask import Flask, render_template, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from uuid import uuid4
from flask import render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    def check_password(self, password):
        print("Stored hash:", self.password_hash)
        print("Provided password hash:", generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Логин уже занят!", "warning")
        else:
            new_user = User(id=str(uuid4()), username=form.username.data)
            new_user.set_password(form.password.data)
            print("Stored hash during registration:", new_user.password_hash)
            db.session.add(new_user)
            db.session.commit()
            flash("Регистрация прошла успешно! Теперь войдите в систему.", "success")
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Provided username:", form.username.data)
        print("Provided password:", form.password.data)
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print("Retrieved user:", user.username)
            print("Password hash from db:", user.password_hash)
            if user.check_password(form.password.data):
                session['user_id'] = user.id
                session['username'] = user.username
                flash("Вы успешно вошли в систему!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Неверный логин или пароль", "danger")
        else:
            flash("Неверный логин или пароль", "danger")
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        if not category:
            flash("Пожалуйста, введите категорию товаров.", "warning")
            return redirect(url_for('dashboard'))

        try:
            # URL для поиска
            url = f"https://www.divan.ru/search?ProductSearch[name]={category}&no_cache=1"
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()  # Проверяем успешность запроса

            # Парсим контент
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('div', class_='_Ud0k')  # Актуальный класс карточки продукта

            results = []
            for product in products:
                title_elem = product.find('span', itemprop='name')
                price_elem = product.find('span', {'data-testid': 'price'})

                title = title_elem.get_text(strip=True) if title_elem else "Название отсутствует"
                price = price_elem.get_text(strip=True) if price_elem else "Цена отсутствует"

                results.append({'title': title, 'price': price})

            if not results:
                flash(f"Товары по категории '{category}' не найдены.", "warning")
                return redirect(url_for('dashboard'))

            return render_template('results.html', products=results, category=category)

        except requests.exceptions.RequestException as e:
            flash(f"Ошибка запроса: {e}", "danger")
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Ошибка парсинга: {e}", "danger")
            return redirect(url_for('dashboard'))

    return render_template('dashboard.html')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host='127.0.0.1', port=5000)