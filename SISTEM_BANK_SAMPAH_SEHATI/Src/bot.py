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

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    
    lapor_handler = ConversationHandler(
        entry_points=[
            CommandHandler("lapor", lapor_start),
            MessageHandler(filters.Regex(r'^(📸 Lapor Sampah|Lapor Sampah)$'), lapor_start)
        ],
        states={ 
            LAPOR: [MessageHandler(filters.ALL & ~filters.COMMAND, lapor_handle)] 
        },
        fallbacks=[CommandHandler("cancel", lapor_cancel)],
        per_chat=True, per_user=True
    )

  
    tambah_handler = ConversationHandler(
        entry_points=[CommandHandler("tambah_produk", tambah_produk_start)],
        states={
            NAMA: [MessageHandler(filters.TEXT & ~filters.COMMAND, tambah_nama)],
            HARGA: [MessageHandler(filters.TEXT & ~filters.COMMAND, tambah_harga)],
            STOK: [MessageHandler(filters.TEXT & ~filters.COMMAND, tambah_stok)],
            DESKRIPSI: [MessageHandler(filters.TEXT & ~filters.COMMAND, tambah_deskripsi)],
            FOTO: [MessageHandler(filters.PHOTO, tambah_foto)],
        },
        fallbacks=[CommandHandler("cancel", tambah_cancel)],
        per_chat=True, per_user=True
    )

    app.add_handler(lapor_handler)
    app.add_handler(tambah_handler)

  
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", my_id))
    app.add_handler(CommandHandler("test_error", trigger_error))
    app.add_handler(CommandHandler("bantuan", bantuan))
    app.add_handler(CommandHandler("katalog", katalog))
    app.add_handler(CommandHandler("hapus_produk", hapus_produk_cmd))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("users", list_users))
    app.add_handler(CommandHandler("reply", reply_user))


    app.add_handler(MessageHandler(filters.Regex(r'^🐞 Lapor Bug$'), trigger_error))
    app.add_handler(MessageHandler(filters.Regex(r'^\d+$') & ~filters.COMMAND, handle_hapus_id))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    app.add_error_handler(error_handler)
    
    print("🚀 Sehati Waste Bot Sedang Berjalan...")
    app.run_polling()

async def send_bug_report_system(error_message):
    try:
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=ADMIN_ID, text=f"🚨 SYSTEM CRASH: {error_message}")
    except: pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        asyncio.run(send_bug_report_system(str(e)))
        raise