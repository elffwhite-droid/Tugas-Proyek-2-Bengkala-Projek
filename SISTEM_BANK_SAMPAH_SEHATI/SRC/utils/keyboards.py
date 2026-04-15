# utils/keyboards.py
from telegram import ReplyKeyboardMarkup

def main_menu():
    keyboard = [
        ["♻️ Jenis Sampah", "💰 Harga"],
        ["📅 Jadwal", "🕒 Jam"],
        ["📚 Edukasi", "🛍️ Katalog"],
        ["📸 Lapor Sampah"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def lapor_keyboard():
    keyboard = [["✅ Selesai Laporan"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)