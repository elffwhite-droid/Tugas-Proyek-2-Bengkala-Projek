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
