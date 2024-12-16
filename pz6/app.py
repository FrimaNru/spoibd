from flask import Flask, render_template, request
from db import init_db, log_request, get_command_stats, get_user_stats

app = Flask(__name__)

# Инициализация базы данных
init_db()

@app.route('/')
def home():
    user_id = request.remote_addr  # Уникальный идентификатор пользователя (IP-адрес)
    log_request(user_id, '/')
    return render_template('index.html')

@app.route('/about')
def about():
    user_id = request.remote_addr
    log_request(user_id, '/about')
    return render_template('about.html')

@app.route('/stats')
def stats():
    user_id = request.remote_addr
    log_request(user_id, '/stats')
    command_stats = get_command_stats()
    user_stats = get_user_stats()
    return render_template('stats.html', command_stats=command_stats, user_stats=user_stats)

if __name__ == '__main__':
    app.run(debug=True)