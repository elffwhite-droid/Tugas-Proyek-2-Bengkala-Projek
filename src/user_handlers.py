from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import simpan_user, simpan_laporan, get_produk
from utils.keyboards import main_menu, lapor_keyboard
from config import ADMIN_ID

LAPOR = 1

JENIS_SAMPAH = """JENIS SAMPAH YANG DITERIMA:\n- Plastik (bersih & kering)\n- Botol\n- Sachet\n- Kertas"""

HARGA_SAMPAH = """HARGA SAAT INI:\n• Plastik : Rp 2.000 / kg\n• Botol   : Rp 3.000 / kg"""

JADWAL = "Pengambilan: Senin, Rabu, Jumat"
JAM = "Jam operasional: 08.00 - 16.00 WIB"
EDUKASI = """Pisahkan sampah organik dan non-organik."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    simpan_user(user.id, user.full_name, user.username)
    await update.message.reply_text(
        "Selamat datang di Sehati Waste Bot!\n\nGunakan menu di bawah:",
        parse_mode="Markdown", reply_markup=main_menu()
    )
    
async def bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gunakan menu atau /lapor untuk mulai", reply_markup=main_menu())

async def jenis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(JENIS_SAMPAH, reply_markup=main_menu())

async def harga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HARGA_SAMPAH, reply_markup=main_menu())

async def jadwal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(JADWAL, reply_markup=main_menu())

async def jam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(JAM, reply_markup=main_menu())

async def edukasi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(EDUKASI, reply_markup=main_menu())

async def katalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_produk()
    if not data:
        await update.message.reply_text("Belum ada produk.", reply_markup=main_menu())
        return
    teks = "KATALOG PRODUK\n"
    for row in data:
        teks += f"{row[1]} - Rp {row[2]:,} | Stok: {row[3]}\n{row[4]}\n\n"
    await update.message.reply_text(teks, parse_mode="Markdown", reply_markup=main_menu())
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text in {"♻️ Jenis Sampah", "Jenis Sampah"}:
        await jenis(update, context)
    elif text in {"💰 Harga", "Harga"}:
        await harga(update, context)
    elif text in {"📅 Jadwal", "Jadwal"}:
        await jadwal(update, context)
    elif text in {"🕒 Jam", "Jam"}:
        await jam(update, context)
    elif text in {"📚 Edukasi", "Edukasi"}:
        await edukasi(update, context)
    elif text in {"🛍️ Katalog", "Katalog"}:
        await katalog(update, context)
    elif text in {"📸 Lapor Sampah", "Lapor Sampah"}:
        await lapor_start(update, context)
    else:
        await update.message.reply_text("Pilihan tidak dikenali.", reply_markup=main_menu())
    
async def lapor_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Mode Laporan Aktif\n\nSilakan kirim teks, foto, atau lokasi. Tekan Selesai Laporan jika sudah selesai.",
        reply_markup=lapor_keyboard()
    )
    return LAPOR

async def lapor_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if text in {"Selesai Laporan", "✅ Selesai Laporan"}:
        await update.message.reply_text("Mode laporan ditutup.", reply_markup=main_menu())
        return ConversationHandler.END
