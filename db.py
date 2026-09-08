import sqlite3
import json
import os

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

def export_to_json():
    conn = sqlite3.connect('pizza_shop.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*), SUM(total_price) FROM orders WHERE status != 'Скасовано'")
    row = cursor.fetchone()
    total_orders = row[0]
    total_revenue = row[1] or 0
    
    cursor.execute('''
        SELECT o.order_id, u.username, o.items, o.total_price, o.status, o.created_at
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        ORDER BY o.order_id DESC LIMIT 50
    ''')
    orders = []
    for r in cursor.fetchall():
        orders.append({
            "id": r[0],
            "username": r[1] or "Невідомий",
            "items": r[2],
            "total": r[3],
            "status": r[4],
            "date": r[5]
        })
    
    data = {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "recent_orders": orders
    }
    
    # Зберігаємо у файл data.json в папку webapp
    json_path = os.path.join(os.path.dirname(__file__), 'webapp', 'data.json')
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    conn.close()

def update_order_status(order_id, status):
    conn = sqlite3.connect('pizza_shop.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE orders SET status = ? WHERE order_id = ?', (status, order_id))
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
