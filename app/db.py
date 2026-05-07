import sqlite3
import os

def get_db_path() -> str:
    return os.getenv('DB_DATABASE', 'app.db')

def get_db() -> sqlite3.Connection:
    return sqlite3.connect(get_db_path())

def init_db():
    conn = get_db()
    conn.execute(
        'CREATE TABLE IF NOT EXISTS books '
        '(id INTEGER PRIMARY KEY, title TEXT, author TEXT, published_year INTEGER)'
    )
    conn.commit()
    conn.close()
