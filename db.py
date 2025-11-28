import sqlite3

DB_NAME = 'todo.db'


def get_db_connection():
    """Створює підключення до бази даних"""
    conn = sqlite3.connect(DB_NAME)
    # Цей рядок дозволяє звертатися до колонок за назвою, а не за індексом
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Створює таблицю та додає тестові дані, якщо їх немає"""
    conn = get_db_connection()

    # Створення таблиці
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS items
                 (
                     id
                     INTEGER
                     PRIMARY
                     KEY
                     AUTOINCREMENT,
                     name
                     TEXT
                     NOT
                     NULL
                 )
                 ''')

    # Перевірка на наявність даних
    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM items')
    count = cursor.fetchone()[0]

    if count == 0:
        print("База порожня. Додаємо тестові дані...")
        conn.execute("INSERT INTO items (name) VALUES ('Купити хліб')")
        conn.execute("INSERT INTO items (name) VALUES ('Вивчити Python')")
        conn.execute("INSERT INTO items (name) VALUES ('Написати код')")
        conn.commit()

    conn.close()