from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

__all__ = ['MAIN_BUTTONS', 'YES_NO_BUTTONS']
MAIN_BUTTONS = ReplyKeyboardMarkup([
        ['/add', '/delete', '/show_all', '/today']
    ], resize_keyboard=True, input_field_placeholder='Выберите действие:')
YES_NO_BUTTONS = ReplyKeyboardMarkup([['Да', 'Нет']], input_field_placeholder='Все корректно?')


def clear_data(user_data: dict) -> None:
    """Clear add data information."""
    user_data.pop('full_name', None)
    user_data.pop('birth_date', None)
    user_data.pop('person_to_delete', None)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    clear_data(context.user_data)
    await update.message.reply_text(
        "Действие отменено.",
        reply_markup=MAIN_BUTTONS
    )
    return ConversationHandler.END
