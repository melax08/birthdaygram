import logging

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from .services import show_all, today_birthdays, next_birthdays
from bot.exceptions import EmptyQuery
from bot.utils import get_user_info
from bot.constants.buttons import (
    MAIN_BUTTONS,
    ALL_BUTTON,
    TODAY_BUTTON,
    WEEK_BUTTON,
    MONTH_BUTTON
)


async def show_all_command(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send a message with all records in database."""
    try:
        message = show_all(update.effective_chat.id)
    except EmptyQuery as error:
        message = [str(error)]

    logging.info(f'Send message about all records '
                 f'to {get_user_info(update)}. Message: {message}')
    await update.message.reply_text('\n'.join(message),
                                    reply_markup=MAIN_BUTTONS)


async def today_birthdays_command(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Sends a message with today birthdays."""
    try:
        message = today_birthdays(update.effective_chat.id)
    except EmptyQuery as error:
        message = [str(error)]

    logging.info(f'Send message about today birthdays '
                 f'to {get_user_info(update)}. Message: {message}')
    await update.message.reply_text('\n'.join(message),
                                    reply_markup=MAIN_BUTTONS)


async def send_next_birthdays_message(update, interval) -> None:
    """Gets DB records for selected interval,
    sends telegram message for user about birthdays in this interval."""
    try:
        message = next_birthdays(update.effective_chat.id, interval)
    except EmptyQuery as error:
        message = [str(error)]

    logging.info(f'Send message about next {interval} days birthdays '
                 f'to {get_user_info(update)}. Message: {message}')

    await update.message.reply_text('\n'.join(message),
                                    reply_markup=MAIN_BUTTONS)


async def next_week_birthday_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Sends a message with birthdays in next 7-days."""
    await send_next_birthdays_message(update, 7)


async def next_month_birthdays_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Sends a message with birthdays in next 30-days."""
    await send_next_birthdays_message(update, 30)


show_all_handler = MessageHandler(
    filters.Regex(ALL_BUTTON) | filters.Regex("/show_all"),
    show_all_command
)

today_handler = MessageHandler(
    filters.Regex(TODAY_BUTTON) | filters.Regex("/today"),
    today_birthdays_command
)

week_handler = MessageHandler(
    filters.Regex(WEEK_BUTTON) | filters.Regex("/week"),
    next_week_birthday_command
)

month_handler = MessageHandler(
    filters.Regex(MONTH_BUTTON) | filters.Regex("/month"),
    next_month_birthdays_command
)
