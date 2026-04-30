import traceback
import html
from datetime import datetime
from config import ADMIN_ID

async def send_error_report(context, error, update=None):
    """Mengirim laporan error profesional dengan Full Traceback"""
    
    # 1. Mengambil detail baris kode (Traceback)
    # Ini yang mencegah laporan muncul 'None'
    tb_list = traceback.format_exception(None, error, error.__traceback__)
    tb_string = "".join(tb_list)

    # 2. Info User
    user_id = update.effective_user.id if update and update.effective_user else "Unknown"
    username = update.effective_user.first_name if update and update.effective_user else "User"

    waktu = datetime.now().strftime("%d %b %Y, %H:%M:%S")
    
    # 3. Format Pesan HTML (Mirip BakulByte)
    message = (
        f"🚨 <b>CRITICAL ERROR — Bank Sampah Sehati</b>\n\n"
        f"⌚ <b>Waktu :</b> {waktu}\n"
        f"📍 <b>Konteks :</b> test_error/zero\n"
        f"👤 <b>User ID :</b> <code>{user_id}</code> ({username})\n"
        f"❌ <b>Error :</b> <code>{html.escape(str(error))}</code>\n"
        f"ℹ️ <b>Info :</b> Terdapat Erorr.\n\n"
        f"📋 <b>Full Traceback:</b>\n"
        f"<pre><code>{html.escape(tb_string)}</code></pre>\n"
        f"✅ <i>Laporan error otomatis dikirim ke admin.</i>"
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=message,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Gagal kirim laporan ke Telegram: {e}")

# Dummy handler agar tidak error saat diimport di bot.py
from telegram.ext import MessageHandler, filters
async def _bug_func(update, context): pass
bug_handler = MessageHandler(filters.COMMAND & filters.Regex(r'bug_dummy'), _bug_func)