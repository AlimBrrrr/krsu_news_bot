import sqlite3


DB_NAME = 'subscribers.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    try:
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                chat_id INTEGER PRIMARY KEY
            )
        ''')

        conn.commit()
    finally:
        conn.close()


def add_subscriber(chat_id) -> bool:
    conn = sqlite3.connect(DB_NAME)
    try:
        cur = conn.cursor()

        cur.execute('INSERT OR IGNORE INTO subscribers (chat_id) VALUES (?)', (chat_id,))
        conn.commit()

        return cur.rowcount == 1
    finally:
        conn.close()


def remove_subscriber(chat_id) -> bool:
    conn = sqlite3.connect(DB_NAME)
    try:
        cur = conn.cursor()

        cur.execute('DELETE FROM subscribers WHERE chat_id = ?', (chat_id,))
        conn.commit()

        return cur.rowcount == 1
    finally:
        conn.close()


def get_subscribers() -> list[int]:
    conn = sqlite3.connect(DB_NAME)
    try:
        cur = conn.cursor()

        cur.execute('SELECT chat_id FROM subscribers')

        return [i[0] for i in cur.fetchall()]
    finally:
        conn.close()
