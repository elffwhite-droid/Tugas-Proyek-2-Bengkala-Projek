# handlers/admin_handlers.py - Dikerjakan oleh Anggota 2
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


# ================= HAPUS PRODUK =================
async def hapus_produk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("? Hanya admin yang boleh.")
        return

    data = get_produk()
    if not data:
        await update.message.reply_text("? Belum ada produk yang bisa dihapus.")
        return

    teks = "??? **Daftar Produk**\nKetik **ID** yang ingin dihapus:\n\n"
    for row in data:
        teks += f"ID: `{row[0]}` | {row[1]} - Rp {row[2]:,}\n"

    teks += "\nContoh: ketik `3` untuk menghapus produk ID 3"

    await update.message.reply_text(teks, parse_mode="Markdown")


async def handle_hapus_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        produk_id = int(update.message.text.strip())
        hapus_produk(produk_id)
        await update.message.reply_text(f"? Produk ID {produk_id} berhasil dihapus!", reply_markup=main_menu())
    except:
        await update.message.reply_text("?? Masukkan hanya angka ID produk.\nContoh: 3")


# ================= BROADCAST =================
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Gunakan: /broadcast [pesan]")
        return

    text = " ".join(context.args)
    users = get_all_users()
    success = 0
    for uid in users:
        try:
            await context.bot.send_message(uid, text)
            success += 1
        except:
            pass
    await update.message.reply_text(f"? Broadcast terkirim ke {success} user.")
