import sqlite3
import os

DB_PATH = "boutique.db"

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clothes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            size TEXT NOT NULL,
            color TEXT NOT NULL,
            date_arrived TEXT NOT NULL,
            total_qty INTEGER NOT NULL,
            sold_qty INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_item(name, price, size, color, date_arrived, total_qty):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clothes (name, price, size, color, date_arrived, total_qty, sold_qty)
        VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (name, price, size, color, date_arrived, total_qty))
    conn.commit()
    conn.close()

def get_all_items():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clothes")
    rows = cursor.fetchall()
    conn.close()
    return rows

def sell_item(item_id, qty_to_sell):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT total_qty, sold_qty FROM clothes WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    if row:
        total_qty, sold_qty = row
        new_sold = sold_qty + qty_to_sell
        if new_sold > total_qty:
            new_sold = total_qty
        cursor.execute("UPDATE clothes SET sold_qty = ? WHERE id = ?", (new_sold, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clothes WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
else:
    init_db()
