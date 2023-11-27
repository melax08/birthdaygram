from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.buttons import MAIN_BUTTONS
from bot.constants.messages import ACTION_CANCELED


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    context.user_data.clear()
    await update.message.reply_text(ACTION_CANCELED, reply_markup=MAIN_BUTTONS)
    return ConversationHandler.END
