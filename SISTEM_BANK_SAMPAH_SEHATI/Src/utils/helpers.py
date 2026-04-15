import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Unhandled exception", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "?? Terjadi kesalahan. Silakan coba lagi nanti."
            )
        except Exception:
            pass


def clean_price(text: str) -> int:
    cleaned = text.replace(".", "").replace(",", "").strip()
    return int(cleaned)
