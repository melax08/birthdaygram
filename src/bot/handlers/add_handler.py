import logging

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.constants.buttons import ADD_BUTTON, MAIN_BUTTONS, YES_NO_BUTTONS
from bot.constants.logging_messages import USER_ADD_LOG
from bot.constants.messages import (
    ADD_CONFIRMATION,
    CLARIFICATION,
    REPEAT_MESSAGE,
    SUCCESS,
    WRITE_BIRTHDATE,
    WRITE_FULL_NAME,
)
from bot.database import UserTable
from bot.exceptions import BirthDateError, FullNameError
from bot.utils import get_user_info
from bot.validators import birth_date_validator, full_name_validator

from .cancel_handler import cancel

FULL_NAME, BIRTHDATE, CONFIRMATION = range(3)


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Entry point of conversation handler for adding a new person to the list of
    birthdates. Asks the user to write the full name of the person to be added.
    """
    await update.message.reply_text(WRITE_FULL_NAME, reply_markup=ReplyKeyboardRemove())
    return FULL_NAME


async def _full_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate entered person full name and asks the user to write the
    birthdate of the person to be added."""
    full_name = update.message.text

    try:
        user_table = await UserTable.get_user_table(update.effective_chat.id)
        await full_name_validator(full_name, user_table)
    except FullNameError as error:
        await update.message.reply_text(str(error))
        return FULL_NAME

    context.user_data["full_name"] = full_name
    await update.message.reply_text(WRITE_BIRTHDATE)

    return BIRTHDATE


async def _birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate entered person birthdate and asks the user to confirm adding
    a new person."""
    birth_date = update.message.text

    try:
        birth_date_db = birth_date_validator(birth_date)
    except BirthDateError as error:
        await update.message.reply_text(str(error))
        return BIRTHDATE

    context.user_data["birth_date"] = birth_date_db
    await update.message.reply_text(
        ADD_CONFIRMATION.format(context.user_data.get("full_name"), birth_date),
        reply_markup=YES_NO_BUTTONS,
    )

    return CONFIRMATION


async def _confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Adds a new person to the list of the user birthdates."""
    answer = update.message.text

    if answer.lower() == "нет":
        context.user_data.clear()
        await update.message.reply_text(REPEAT_MESSAGE)
        return FULL_NAME
    elif answer.lower() == "да":
        user_table = await UserTable.get_user_table(update.effective_chat.id)
        await user_table.add_person(
            context.user_data.get("full_name"), context.user_data.get("birth_date")
        )
        logging.info(
            USER_ADD_LOG.format(
                get_user_info(update),
                context.user_data.get("full_name"),
                context.user_data.get("birth_date"),
            )
        )
        context.user_data.clear()
        await update.message.reply_text(SUCCESS, reply_markup=MAIN_BUTTONS)
        return ConversationHandler.END
    else:
        await update.message.reply_text(CLARIFICATION, reply_markup=YES_NO_BUTTONS)
        return CONFIRMATION


add_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex(ADD_BUTTON) | filters.Regex("/add"), add_command)
    ],
    states={
        FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, _full_name)],
        BIRTHDATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, _birth_date)],
        CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, _confirmation)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
