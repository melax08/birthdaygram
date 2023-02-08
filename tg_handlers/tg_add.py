from telegram import Update
from telegram.ext import (CommandHandler, ContextTypes, MessageHandler,
                          filters, ConversationHandler)

from db_actions import Database
from exceptions import BirthDateError, FullNameError
from validators import birth_date_validator, full_name_validator
from .misc import YES_NO_BUTTONS, MAIN_BUTTONS, cancel, clear_data

FULL_NAME, BIRTHDATE, CONFIRMATION = range(3)


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Напишите полное имя человека, '
                                    'для отмены /cancel')
    return FULL_NAME


async def _full_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    full_name = update.message.text
    try:
        full_name_validator(full_name)
    except FullNameError as error:
        await update.message.reply_text(str(error))
        return FULL_NAME
    context.user_data["full_name"] = full_name
    await update.message.reply_text('Напишите дату рождения человека в '
                                    'формате dd.mm.yyyy, для отмены /cancel')
    return BIRTHDATE


async def _birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    birth_date = update.message.text
    try:
        birth_date_db = birth_date_validator(birth_date)
    except BirthDateError as error:
        await update.message.reply_text(str(error))
        return BIRTHDATE
    context.user_data["birth_date"] = birth_date_db
    await update.message.reply_text(f'Вы добавили: '
                                    f'{context.user_data.get("full_name")}, '
                                    f'дата рождения: {birth_date}. '
                                    f'Все верно?', reply_markup=YES_NO_BUTTONS)
    return CONFIRMATION


async def _confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text
    if answer.lower() == 'нет':
        clear_data(context.user_data)
        await update.message.reply_text('В таком случае, заполните все '
                                        'сначала. Напишите имя человека.')
        return FULL_NAME
    elif answer.lower() == 'да':
        db = Database()
        db.new_record(context.user_data.get("full_name"),
                      context.user_data.get("birth_date"))
        clear_data(context.user_data)
        await update.message.reply_text('✅ Успешно!',
                                        reply_markup=MAIN_BUTTONS)
        return ConversationHandler.END
    else:
        await update.message.reply_text('Ответьте, Да или Нет.',
                                        reply_markup=YES_NO_BUTTONS)
        return CONFIRMATION


add_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("add", add_command)],
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
