from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import logging
import asyncio
from telegram import Bot, Update
from config import TOKEN, ADMIN_ID

from handlers.user_handlers import (
    start, bantuan, katalog,
    lapor_start, lapor_handle, lapor_cancel, handle_menu,
    LAPOR  
)

from admin_handlers import (
    tambah_produk_start, tambah_nama, tambah_harga, tambah_stok, 
    tambah_deskripsi, tambah_foto, tambah_cancel,
    hapus_produk_cmd, handle_hapus_id, broadcast, reply_user, list_users, my_id,
    NAMA, HARGA, STOK, DESKRIPSI, FOTO 
)

from bug_report import send_error_report

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    if not context.error: return
    logging.error("Exception detected:", exc_info=context.error)
    try:
        await send_error_report(context, context.error, update if isinstance(update, Update) else None)
    except Exception as e:
        logging.error(f"Gagal kirim report: {e}")

async def trigger_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Menjalankan simulasi error...")
    try:
        result = 1 / 0
    except Exception as e:
        await send_error_report(context, e, update)
        await update.message.reply_text(f"✅ Simulasi selesai. Error: {type(e).__name__}")