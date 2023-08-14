import logging

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters)

from bot.constants.buttons import ADD_BUTTON, MAIN_BUTTONS, YES_NO_BUTTONS
from bot.constants.messages import (ADD_CONFIRMATION, CLARIFICATION,
                                    REPEAT_MESSAGE, SUCCESS, WRITE_BIRTHDATE,
                                    WRITE_FULL_NAME)
from bot.database import UserTable
from bot.exceptions import BirthDateError, FullNameError
from bot.validators import birth_date_validator, full_name_validator

from .cancel_handler import cancel

FULL_NAME, BIRTHDATE, CONFIRMATION = range(3)


async def add_command(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.message.reply_text(
        WRITE_FULL_NAME,
        reply_markup=ReplyKeyboardRemove()
    )
    return FULL_NAME


async def _full_name(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    full_name = update.message.text

    try:
        full_name_validator(full_name)
    except FullNameError as error:
        await update.message.reply_text(str(error))
        return FULL_NAME

    context.user_data["full_name"] = full_name
    await update.message.reply_text(WRITE_BIRTHDATE)

    return BIRTHDATE


async def _birth_date(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    birth_date = update.message.text

    try:
        birth_date_db = birth_date_validator(birth_date)
    except BirthDateError as error:
        await update.message.reply_text(str(error))
        return BIRTHDATE

    context.user_data["birth_date"] = birth_date_db
    await update.message.reply_text(
        ADD_CONFIRMATION.format(context.user_data.get("full_name"),
                                birth_date),
        reply_markup=YES_NO_BUTTONS
    )

    return CONFIRMATION


async def _confirmation(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    answer = update.message.text

    if answer.lower() == 'нет':
        context.user_data.clear()
        await update.message.reply_text(REPEAT_MESSAGE)
        return FULL_NAME
    elif answer.lower() == 'да':
        user_table = UserTable(update.effective_chat.id)
        user_table.add_person(
            context.user_data.get("full_name"),
            context.user_data.get("birth_date")
        )
        logging.info(
            f'User {update.effective_user.id} '
            f'add {context.user_data.get("full_name")} '
            f'{context.user_data.get("birth_date")}'
        )
        context.user_data.clear()
        await update.message.reply_text(SUCCESS, reply_markup=MAIN_BUTTONS)
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            CLARIFICATION,
            reply_markup=YES_NO_BUTTONS
        )
        return CONFIRMATION


add_handler = ConversationHandler(
    # entry_points=[CommandHandler("add", add_command)],
    entry_points=[MessageHandler(
        filters.Regex(ADD_BUTTON) | filters.Regex('/add'), add_command)],
    states={
        FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                   _full_name)],
        BIRTHDATE: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                   _birth_date)],
        CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                      _confirmation)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
