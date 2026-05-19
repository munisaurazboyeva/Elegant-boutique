import os

# Azure SQL ulanish sozlamalari
AZURE_SERVER   = "demo-azure-3testing.database.windows.net"
AZURE_DATABASE = "boutiquedb"
AZURE_USERNAME = "azure-admin"
AZURE_PASSWORD = "munisa-006"
AZURE_DRIVER   = "{ODBC Driver 18 for SQL Server}"

USE_AZURE = True   # Azure SQL faol — True=Azure, False=SQLite

# ─── SQLite zaxira ────────────────────────────────────────────────────────────
import sqlite3
DB_PATH = os.path.join(os.path.dirname(__file__), "boutique.db")

def _sqlite_connect():
    return sqlite3.connect(DB_PATH)

# ─── Azure SQL ulanish ────────────────────────────────────────────────────────
def _azure_connect():
    import pyodbc
    conn_str = (
        f"DRIVER={AZURE_DRIVER};"
        f"SERVER={AZURE_SERVER};"
        f"DATABASE={AZURE_DATABASE};"
        f"UID={AZURE_USERNAME};"
        f"PWD={AZURE_PASSWORD};"
        "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    return pyodbc.connect(conn_str)

def connect():
    if USE_AZURE:
        return _azure_connect()
    return _sqlite_connect()

# ─── Ma'lumotlar bazasini boshlash ────────────────────────────────────────────
def init_db():
    conn = connect()
    cursor = conn.cursor()
    if USE_AZURE:
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='clothes')
            CREATE TABLE clothes (
                id         INT IDENTITY(1,1) PRIMARY KEY,
                name       NVARCHAR(200) NOT NULL,
                price      INT           NOT NULL,
                size       NVARCHAR(20)  NOT NULL,
                color      NVARCHAR(50)  NOT NULL,
                date_arrived NVARCHAR(20) NOT NULL,
                total_qty  INT           NOT NULL,
                sold_qty   INT           NOT NULL DEFAULT 0
            )
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clothes (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT    NOT NULL,
                price        INTEGER NOT NULL,
                size         TEXT    NOT NULL,
                color        TEXT    NOT NULL,
                date_arrived TEXT    NOT NULL,
                total_qty    INTEGER NOT NULL,
                sold_qty     INTEGER NOT NULL DEFAULT 0
            )
        """)
    conn.commit()
    conn.close()

# ─── CRUD funksiyalar ─────────────────────────────────────────────────────────
def add_item(name, price, size, color, date_arrived, total_qty):
    conn = connect()
    cursor = conn.cursor()
    if USE_AZURE:
        cursor.execute("""
            INSERT INTO clothes (name, price, size, color, date_arrived, total_qty, sold_qty)
            VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (name, price, size, color, date_arrived, total_qty))
    else:
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

# ─── Avtomatik ishga tushirish ────────────────────────────────────────────────
init_db()
