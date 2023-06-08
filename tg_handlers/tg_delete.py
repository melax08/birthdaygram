from telegram import Update
from telegram.ext import (CommandHandler, ContextTypes, MessageHandler,
                          filters, ConversationHandler)

from alchemy_actions import UserTable
from .misc import YES_NO_BUTTONS, MAIN_BUTTONS, cancel, clear_data

FULL_NAME, CONFIRMATION = range(2)


async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Напишите полное имя человека, которого '
                                    'хотите удалить из списка. '
                                    'Для отмены /cancel')
    return FULL_NAME


async def _full_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    full_name = update.message.text
    user_table = UserTable(update.effective_chat.id)
    person = user_table.select_person(full_name)
    if not person:
        await update.message.reply_text('Указанное имя не найдено в базе. '
                                        'Введите новое имя, или /cancel')
        return FULL_NAME
    else:
        context.user_data["person_to_delete"] = person
        await update.message.reply_text(f'Произвести удаление {person.full_name}, дата рождения: {person.birth_date:%d.%m.%Y}?',
                                        reply_markup=YES_NO_BUTTONS)
    return CONFIRMATION


async def _confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text
    if answer.lower() == 'нет':
        clear_data(context.user_data)
        await update.message.reply_text('Действие отменено.',
                                        reply_markup=MAIN_BUTTONS)
        return ConversationHandler.END
    elif answer.lower() == 'да':
        user_table = UserTable(update.effective_chat.id)
        user_table.delete_person(context.user_data.get("person_to_delete"))
        clear_data(context.user_data)
        await update.message.reply_text('✅ Успешно!',
                                        reply_markup=MAIN_BUTTONS)
        return ConversationHandler.END
    else:
        await update.message.reply_text('Ответьте, Да или Нет.',
                                        reply_markup=YES_NO_BUTTONS)
        return CONFIRMATION


delete_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("delete", delete_command)],
    states={
        FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                   _full_name)],
        CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                      _confirmation)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
