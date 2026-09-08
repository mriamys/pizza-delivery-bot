import sqlite3


def init_db():
    conn = sqlite3.connect("pizza.db")
    cursor = conn.cursor()
    # Створюємо таблицю замовлень
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            items TEXT,
            total_price INTEGER,
            status TEXT DEFAULT 'Нове'
        )
    """)
    conn.commit()
    conn.close()


def add_order(user_id, username, items, total_price):
    conn = sqlite3.connect("pizza.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO orders (user_id, username, items, total_price)
        VALUES (?, ?, ?, ?)
    """,
        (user_id, username, items, total_price),
    )
    conn.commit()
    conn.close()


def get_orders():
    conn = sqlite3.connect("pizza.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, items, total_price, status FROM orders ORDER BY id DESC LIMIT 10"
    )
    orders = cursor.fetchall()
    conn.close()
    return orders
