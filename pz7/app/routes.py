from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.models import User
from app import db
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required
from uuid import uuid4
import requests
from bs4 import BeautifulSoup

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Вы успешно вошли в систему!", "success")
            return redirect(url_for('main.dashboard'))
        flash("Неверный логин или пароль", "danger")
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Логин уже занят!", "warning")
        else:
            new_user = User(id=str(uuid4()), username=form.username.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash("Регистрация прошла успешно!", "success")
            return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        if not category:
            flash("Пожалуйста, введите категорию товаров.", "warning")
            return redirect(url_for('main.dashboard'))

        try:
            url = f"https://www.divan.ru/search?ProductSearch[name]={category}&no_cache=1"
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('div', class_='_Ud0k')

            results = []
            for product in products:
                title_elem = product.find('span', itemprop='name')
                price_elem = product.find('span', {'data-testid': 'price'})

                title = title_elem.get_text(strip=True) if title_elem else "Название отсутствует"
                price = price_elem.get_text(strip=True) if price_elem else "Цена отсутствует"

                results.append({'title': title, 'price': price})

            if not results:
                flash(f"Товары по категории '{category}' не найдены.", "warning")
                return redirect(url_for('main.dashboard'))

            return render_template('results.html', products=results, category=category)

        except requests.exceptions.RequestException as e:
            flash(f"Ошибка запроса: {e}", "danger")
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            flash(f"Ошибка парсинга: {e}", "danger")
            return redirect(url_for('main.dashboard'))

    return render_template('dashboard.html')
