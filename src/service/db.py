import sqlite3
import json

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

    conn.execute('''
                 CREATE TABLE IF NOT EXISTS idempotency_keys
                 (
                     key
                     TEXT
                     PRIMARY
                     KEY,
                     status_code
                     INTEGER,
                     response_body
                     TEXT,
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


def get_idempotency_key(key):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM idempotency_keys WHERE key = ?', (key,)).fetchone()
    conn.close()

    if row:
        return {
            "status_code": row["status_code"],
            "response_body": json.loads(row["response_body"])
        }
    return None


def save_idempotency_key(key, status_code, response_body):
    conn = get_db_connection()
    conn.execute(
        '''INSERT OR REPLACE INTO idempotency_keys 
           (key, status_code, response_body, created_at) 
           VALUES (?, ?, ?, datetime("now"))''',
        (key, status_code, json.dumps(response_body))
    )
    conn.commit()
    conn.close()