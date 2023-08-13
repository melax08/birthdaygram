import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (CommandHandler, ContextTypes, MessageHandler,
                          filters, ConversationHandler)

from bot.database import UserTable
from bot.constants.buttons import MAIN_BUTTONS, YES_NO_BUTTONS, DELETE_BUTTON
from bot.constants.messages import (
    WRITE_FULL_NAME_TO_DELETE,
    PERSON_NOT_FOUND,
    ACTION_CANCELED,
    SUCCESS,
    REPEAT_MESSAGE,
    DELETE_CONFIRMATION
)
from bot.constants.constants import DATE_FORMAT
from .cancel_handler import cancel

FULL_NAME, CONFIRMATION = range(2)


async def delete_command(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.message.reply_text(
        WRITE_FULL_NAME_TO_DELETE,
        reply_markup=ReplyKeyboardRemove()
    )
    return FULL_NAME


async def _full_name(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    full_name = update.message.text
    user_table = UserTable(update.effective_chat.id)
    person = user_table.select_person(full_name)
    if not person:
        await update.message.reply_text(PERSON_NOT_FOUND)
        return FULL_NAME
    else:
        context.user_data["person_to_delete"] = person
        await update.message.reply_text(
            DELETE_CONFIRMATION.format(
                person.full_name,
                person.birth_date.strftime(DATE_FORMAT)
            ),
            reply_markup=YES_NO_BUTTONS
        )
    return CONFIRMATION


async def _confirmation(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text
    if answer.lower() == 'нет':
        context.user_data.clear()
        await update.message.reply_text(ACTION_CANCELED,
                                        reply_markup=MAIN_BUTTONS)
        return ConversationHandler.END
    elif answer.lower() == 'да':
        user_table = UserTable(update.effective_chat.id)
        user_table.delete_person(context.user_data.get("person_to_delete"))
        logging.info(
            f'User {update.effective_user.id} '
            f'delete {context.user_data.get("person_to_delete")}'
        )
        context.user_data.clear()
        await update.message.reply_text(SUCCESS,
                                        reply_markup=MAIN_BUTTONS)
        return ConversationHandler.END
    else:
        await update.message.reply_text(REPEAT_MESSAGE,
                                        reply_markup=YES_NO_BUTTONS)
        return CONFIRMATION


delete_handler = ConversationHandler(
    entry_points=[MessageHandler(
        filters.Regex(DELETE_BUTTON) | filters.Regex('/delete'),
        delete_command)
    ],
    states={
        FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                   _full_name)],
        CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                      _confirmation)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
