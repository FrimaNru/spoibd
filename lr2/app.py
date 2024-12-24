import threading
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from extensions import db
from models import Fact, Admin, BotMessage
from telegram_bot import run_bot

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://047084354_zvir:Arti2005@mysql.j1007852.myjino.ru:3306/j1007852_237_zvir"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "e2c4b9274f1e7b6a8b9f0d4f7c3a9d12"
db.init_app(app)

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session['user'] = {'username': admin.username, 'role': admin.role}
            return redirect(url_for('dashboard'))
        else:
            flash('Неверный логин или пароль!', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if Admin.query.filter_by(username=username).first():
            flash('Логин уже занят!', 'danger')
        else:
            new_admin = Admin(username=username, password=password, role=role)
            db.session.add(new_admin)
            db.session.commit()
            flash('Вы успешно зарегистрировались!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/facts', methods=['GET', 'POST'])
def facts():
    if request.method == 'POST':
        fact_text = request.form.get('fact_text')
        if fact_text:
            new_fact = Fact(text=fact_text)
            db.session.add(new_fact)
            db.session.commit()
            return redirect(url_for('facts'))
    all_facts = Fact.query.all()
    user = session.get('user')
    return render_template('facts.html', facts=all_facts, user=user)

@app.route('/delete_fact/<string:fact_id>', methods=['POST'])
def delete_fact(fact_id):
    fact_to_delete = Fact.query.get(fact_id)
    if fact_to_delete:
        db.session.delete(fact_to_delete)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@app.route('/statistics')
def statistics():
    messages = BotMessage.query.order_by(BotMessage.timestamp.desc()).all()
    user = session.get('user')
    return render_template('statistics.html', messages=messages, user=user)

if __name__ == "__main__":
    # Создаем поток для запуска бота
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True 
    bot_thread.start()

    # Запускаем Flask
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
