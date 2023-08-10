from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

__all__ = ['MAIN_BUTTONS', 'YES_NO_BUTTONS', 'ADD_BTN', 'DELETE_BTN',
           'ALL_BTN', 'TODAY_BTN', 'WEEK_BTN', 'MONTH_BTN', 'HELP_BTN']

ADD_BTN = '✅ Добавить'
DELETE_BTN = '❌ Удалить'
ALL_BTN = '🗂 Список'
TODAY_BTN = 'Сегодня'
WEEK_BTN = 'Неделя'
MONTH_BTN = 'Месяц'
HELP_BTN = '❓ Помощь'

MAIN_BUTTONS = ReplyKeyboardMarkup([
        [ADD_BTN, DELETE_BTN, ALL_BTN],
        [TODAY_BTN, WEEK_BTN, MONTH_BTN],
        [HELP_BTN]
    ], resize_keyboard=True, input_field_placeholder='Выберите действие:')
YES_NO_BUTTONS = ReplyKeyboardMarkup([['Да', 'Нет']],
                                     resize_keyboard=True,
                                     input_field_placeholder='Все корректно?')


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    context.user_data.clear()
    await update.message.reply_text(
        "Действие отменено.",
        reply_markup=MAIN_BUTTONS
    )
    return ConversationHandler.END
