import sqlite3

DB_NAME = 'todo.db'


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute('''
                 CREATE TABLE IF NOT EXISTS tasks
                 (
                     id
                     TEXT
                     PRIMARY
                     KEY,
                     title
                     TEXT
                     NOT
                     NULL,
                     priority
                     TEXT
                     DEFAULT
                     'normal',
                     is_completed
                     BOOLEAN
                     DEFAULT
                     0,
                     created_at
                     TEXT
                 )
                 ''')

    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM tasks')
    count = cursor.fetchone()[0]

    if count == 0:
        conn.execute(
            "INSERT INTO tasks (id, title, priority, created_at) VALUES (?, ?, ?, ?)",
            ('t-test1', 'Вивчити Python', 'high', '2025-12-03T12:00:00Z')
        )
        conn.execute(
            "INSERT INTO tasks (id, title, priority, created_at) VALUES (?, ?, ?, ?)",
            ('t-test2', 'Написати код', 'normal', '2025-12-03T13:00:00Z')
        )
        conn.commit()

    conn.close()