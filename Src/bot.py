# bot.py - File Utama Bot (Dibuat oleh Anggota 3)
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
import logging

from config import TOKEN
from handlers.user_handlers import (
    start, bantuan, jenis, harga, jadwal, jam, edukasi, katalog,
    lapor_start, lapor_handle, lapor_cancel, handle_menu
)
from admin_handlers import (
    tambah_produk_start, tambah_nama, tambah_harga, tambah_stok, tambah_deskripsi, tambah_cancel,
    hapus_produk_cmd, handle_hapus_id, broadcast
)
from utils.keyboards import main_menu, lapor_keyboard
from utils.helpers import global_error_handler

# States
LAPOR = 1
NAMA, HARGA, STOK, DESKRIPSI = range(4)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Lapor Conversation
    lapor_handler = ConversationHandler(
        entry_points=[CommandHandler("lapor", lapor_start)],
        states={
            LAPOR: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, lapor_handle),
                MessageHandler(filters.PHOTO, lapor_handle),
                MessageHandler(filters.LOCATION, lapor_handle),
            ]
        },
        fallbacks=[CommandHandler("cancel", lapor_cancel)],
        per_chat=True,
        per_user=True
    )

    # Tambah Produk Conversation
    tambah_handler = ConversationHandler(
        entry_points=[CommandHandler("tambah_produk", tambah_produk_start)],
        states={
            NAMA: [MessageHandler(filters.TEXT & ~filters.COMMAND, tambah_nama)],
            HARGA: [MessageHandler(filters.TEXT & ~filters.COMMAND, tambah_harga)],
            STOK: [MessageHandler(filters.TEXT & ~filters.COMMAND, tambah_stok)],
            DESKRIPSI: [MessageHandler(filters.TEXT & ~filters.COMMAND, tambah_deskripsi)],
        },
        fallbacks=[CommandHandler("cancel", tambah_cancel)],
        per_chat=True,
        per_user=True
    )

    # Daftarkan semua handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bantuan", bantuan))
    app.add_handler(CommandHandler("jenis_sampah", jenis))
    app.add_handler(CommandHandler("harga", harga))
    app.add_handler(CommandHandler("jadwal", jadwal))
    app.add_handler(CommandHandler("jam", jam))
    app.add_handler(CommandHandler("edukasi", edukasi))
    app.add_handler(CommandHandler("katalog", katalog))
    app.add_handler(CommandHandler("hapus_produk", hapus_produk_cmd))
    app.add_handler(CommandHandler("broadcast", broadcast))

    app.add_handler(lapor_handler)
    app.add_handler(tambah_handler)

    # Handler hapus produk dengan ID
    app.add_handler(MessageHandler(filters.Regex(r'^\d+$') & ~filters.COMMAND, handle_hapus_id))

    # Menu Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    # Global Error Handler
    app.add_error_handler(global_error_handler)

    print("?? Sehati Waste Bot sedang berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
