import sqlite3

def init_db():
    conn = sqlite3.connect('pizza_shop.db')
    cursor = conn.cursor()
    
    # Таблиця користувачів
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT
    )
    ''')
    
    # Таблиця замовлень
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        items TEXT,
        total_price INTEGER,
        status TEXT DEFAULT 'Нове',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name):
    conn = sqlite3.connect('pizza_shop.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)',
                   (user_id, username, first_name))
    conn.commit()
    conn.close()

def add_order(user_id, items, total_price):
    conn = sqlite3.connect('pizza_shop.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (user_id, items, total_price) VALUES (?, ?, ?)',
                   (user_id, items, total_price))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('pizza_shop.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM orders')
    total_orders = cursor.fetchone()[0]
    cursor.execute('SELECT SUM(total_price) FROM orders')
    total_revenue = cursor.fetchone()[0] or 0
    conn.close()
    return total_orders, total_revenue
