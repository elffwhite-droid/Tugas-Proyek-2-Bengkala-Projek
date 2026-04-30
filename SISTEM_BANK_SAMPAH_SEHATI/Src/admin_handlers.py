# handlers/admin_handlers.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import tambah_produk, get_produk, hapus_produk, get_all_users
from utils.keyboards import main_menu
from utils.helpers import clean_price
from config import ADMIN_ID

# State untuk percakapan (0 sampai 4)
# Pastikan ada 5 tahapan (NAMA sampai FOTO)
NAMA, HARGA, STOK, DESKRIPSI, FOTO = range(5)

# ================= TAMBAH PRODUK =================
async def tambah_produk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Hanya admin yang boleh menambahkan produk.")
        return ConversationHandler.END

    await update.message.reply_text("📦 Masukkan **nama produk**:")
    return NAMA

async def tambah_nama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nama'] = update.message.text.strip()
    await update.message.reply_text("💰 Masukkan **harga** (angka saja):")
    return HARGA

async def tambah_harga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Gunakan fungsi helper atau int() untuk membersihkan input harga
        context.user_data['harga'] = int(update.message.text.replace('.', '').replace(',', ''))
        await update.message.reply_text("🔢 Masukkan **stok**:")
        return STOK
    except:
        await update.message.reply_text("❌ Harga harus berupa angka. Masukkan lagi:")
        return HARGA

async def tambah_stok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['stok'] = int(update.message.text.strip())
        await update.message.reply_text("📝 Masukkan **deskripsi produk**:")
        return DESKRIPSI
    except:
        await update.message.reply_text("❌ Stok harus berupa angka. Masukkan lagi:")
        return STOK

async def tambah_deskripsi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['deskripsi'] = update.message.text.strip()
    await update.message.reply_text("📸 Kirimkan **foto produk**:")
    return FOTO

async def tambah_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Cek apakah yang dikirim benar-benar foto
    if not update.message.photo:
        await update.message.reply_text("❌ Mohon kirimkan **FOTO** produk:")
        return FOTO
    
    # Ambil ID foto ukuran terbesar
    foto_id = update.message.photo[-1].file_id
    
    try:
        # MEMANGGIL DATABASE (Pastikan di database.py sudah ada 5 kolom)
        tambah_produk(
            context.user_data['nama'],
            context.user_data['harga'],
            context.user_data['stok'],
            context.user_data['deskripsi'],
            foto_id
        )
        await update.message.reply_text("✅ Produk berhasil ditambahkan ke katalog!", reply_markup=main_menu())
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal menyimpan ke database: {e}")

    context.user_data.clear()
    return ConversationHandler.END

async def tambah_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Penambahan produk dibatalkan.", reply_markup=main_menu())
    context.user_data.clear()
    return ConversationHandler.END

# ================= TOOLS ADMIN =================
async def hapus_produk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    data = get_produk()
    if not data:
        await update.message.reply_text("📂 Katalog masih kosong.")
        return
    teks = "🗑️ **Daftar Produk**\nKetik **ID** produk untuk menghapus:\n\n"
    for r in data: 
        teks += f"ID: `{r[0]}` | {r[1]}\n"
    await update.message.reply_text(teks, parse_mode="Markdown")

async def handle_hapus_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try:
        produk_id = int(update.message.text)
        hapus_produk(produk_id)
        await update.message.reply_text(f"✅ Produk ID {produk_id} berhasil dihapus.")
    except: 
        await update.message.reply_text("❌ Masukkan angka ID produk yang valid.")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID or not context.args: return
    pesan = " ".join(context.args)
    users = get_all_users()
    count = 0
    for uid in users:
        try: 
            await context.bot.send_message(uid, f"📢 **PENGUMUMAN ADMIN**\n\n{pesan}", parse_mode="Markdown")
            count += 1
        except: pass
    await update.message.reply_text(f"📢 Berhasil mengirim pesan ke {count} pengguna.")

async def reply_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID or len(context.args) < 2: 
        await update.message.reply_text("Format: `/reply [ID] [Pesan]`", parse_mode="Markdown")
        return
    try:
        u_id = int(context.args[0])
        msg = " ".join(context.args[1:])
        await context.bot.send_message(u_id, f"📩 **Balasan dari Admin:**\n\n{msg}", parse_mode="Markdown")
        await update.message.reply_text(f"✅ Pesan terkirim ke {u_id}.")
    except Exception as e: 
        await update.message.reply_text(f"❌ Gagal mengirim: {e}")

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    users = get_all_users()
    teks = "👥 **Daftar User ID:**\n\n" + "\n".join([f"`{u}`" for u in users])
    await update.message.reply_text(teks, parse_mode="Markdown")

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 ID Kamu: `{update.effective_user.id}`", parse_mode="Markdown")