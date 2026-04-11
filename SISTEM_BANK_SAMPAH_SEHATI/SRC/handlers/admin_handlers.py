from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import tambah_produk, get_produk, hapus_produk, get_all_users
from utils.keyboards import main_menu, lapor_keyboard
from utils.helpers import clean_price
from config import ADMIN_ID

NAMA, HARGA, STOK, DESKRIPSI = range(4)

# ================= TAMBAH PRODUK =================
async def tambah_produk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("? Hanya admin yang boleh menambahkan produk.")
        return ConversationHandler.END

    await update.message.reply_text("??? Masukkan **nama produk**:")
    return NAMA


async def tambah_nama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("? Hanya admin yang boleh.")
        context.user_data.clear()
        return ConversationHandler.END

    context.user_data['nama'] = update.message.text.strip()
    await update.message.reply_text("?? Masukkan **harga** (boleh pakai titik):\nContoh: 50000 atau 50.000")
    return HARGA

async def tambah_harga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("? Hanya admin yang boleh.")
        context.user_data.clear()
        return ConversationHandler.END

    try:
        context.user_data['harga'] = clean_price(update.message.text)
        await update.message.reply_text("?? Masukkan **stok** (angka saja):")
        return STOK
    except:
        await update.message.reply_text("?? Harga harus berupa angka. Coba lagi:")
        return HARGA
    
async def tambah_stok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("? Hanya admin yang boleh.")
        context.user_data.clear()
        return ConversationHandler.END

    try:
        context.user_data['stok'] = int(update.message.text.strip())
        await update.message.reply_text("?? Masukkan **deskripsi** produk:")
        return DESKRIPSI
    except:
        await update.message.reply_text("?? Stok harus angka. Coba lagi:")
        return STOK
    
async def tambah_deskripsi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("? Hanya admin yang boleh.")
        context.user_data.clear()
        return ConversationHandler.END

    nama = context.user_data.get('nama')
    harga = context.user_data.get('harga')
    stok = context.user_data.get('stok')
    deskripsi = update.message.text.strip()
    
    tambah_produk(nama, harga, stok, deskripsi)
    
    await update.message.reply_text(
        f"? Produk berhasil ditambahkan!\n\n"
        f"Nama: {nama}\n"
        f"Harga: Rp {harga:,}\n"
        f"Stok: {stok}\n"
        f"Deskripsi: {deskripsi}",
        reply_markup=main_menu()
    )
    context.user_data.clear()
    return ConversationHandler.END

async def tambah_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("? Proses tambah produk dibatalkan.", reply_markup=main_menu())
    context.user_data.clear()
    return ConversationHandler.END