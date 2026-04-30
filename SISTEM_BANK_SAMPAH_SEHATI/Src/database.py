import sqlite3
from datetime import datetime

conn = sqlite3.connect("sehati.db", check_same_thread=False)
cursor = conn.cursor()

# ================= TABEL =================
# Menambahkan kolom foto_id agar katalog punya gambar
cursor.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    harga INTEGER,
    stok INTEGER,
    deskripsi TEXT,
    foto_id TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    full_name TEXT,
    username TEXT,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS laporan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    full_name TEXT,
    message TEXT,
    photo_file_id TEXT,
    latitude REAL,
    longitude REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# ================= FUNGSI DATABASE =================
def tambah_produk(nama, harga, stok, deskripsi, foto_id):
    cursor.execute(
        "INSERT INTO produk (nama, harga, stok, deskripsi, foto_id) VALUES (?, ?, ?, ?, ?)",
        (nama, harga, stok, deskripsi, foto_id)
    )
    conn.commit()
    

def get_produk():
    cursor.execute("SELECT * FROM produk")
    return cursor.fetchall()


def hapus_produk(produk_id: int):
    cursor.execute("DELETE FROM produk WHERE id = ?", (produk_id,))
    conn.commit()


def simpan_user(user_id, full_name, username):
    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, full_name, username)
        VALUES (?, ?, ?)
    """, (user_id, full_name, username))
    conn.commit()


def simpan_laporan(user_id, full_name, message=None, photo_file_id=None, latitude=None, longitude=None):
    cursor.execute("""
        INSERT INTO laporan (user_id, full_name, message, photo_file_id, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, full_name, message, photo_file_id, latitude, longitude))
    conn.commit()


def get_all_users():
    cursor.execute("SELECT user_id FROM users")
    return [row[0] for row in cursor.fetchall()]