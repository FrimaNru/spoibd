import sqlite3
from datetime import datetime

DB_NAME = "stats.db"

def init_db():
    """Инициализация базы данных."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблица для статистики пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            route TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_request(user_id, route):
    """Логирование запроса."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("INSERT INTO user_stats (user_id, route, timestamp) VALUES (?, ?, ?)", (user_id, route, timestamp))
    conn.commit()
    conn.close()

def get_command_stats():
    """Собирает статистику по командам (маршрутам)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT route, DATE(timestamp) as date, COUNT(*) as count
        FROM user_stats
        GROUP BY route, DATE(timestamp)
        ORDER BY date DESC
    """)
    stats = cursor.fetchall()
    conn.close()
    return stats

def get_user_stats():
    """Собирает общую статистику по пользователям."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, DATE(timestamp) as date, COUNT(*) as count
        FROM user_stats
        GROUP BY user_id, DATE(timestamp)
        ORDER BY date DESC
    """)
    stats = cursor.fetchall()
    conn.close()
    return stats