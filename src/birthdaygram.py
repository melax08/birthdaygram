import logging

from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters,)

from alchemy_actions import UserTable
from utils import create_persons_info_list, check_today_birthdays
from tg_handlers import add_conv_handler, delete_conv_handler, MAIN_BUTTONS
from constants import TOKEN
from configs import configure_logging


def _get_user_info(update: Update) -> str:
    """Collects information about telegram user and makes string."""
    info = update.message
    return (f'{info.chat.username}, {info.chat.first_name} '
            f'{info.chat.last_name}, {update.effective_user.id}')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start or /help is issued."""
    user = update.effective_user
    logging.info(f'Someone starts bot: {_get_user_info(update)}')
    await update.message.reply_html(
        f"👋 Привет {user.mention_html()}!\n\n"
        f"<b>Команды бота</b>\n"
        f"/add - добавить человека в список\n"
        f"/delete - удалить человека из списка\n"
        f"/show_all - посмотреть список дней рождений\n\n"
        f"Когда у кого-то из списка будет день рождения, "
        f"я сообщу тебе об этом.",
        reply_markup=MAIN_BUTTONS
    )


# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /help is issued."""
#     await update.message.reply_text("There is some help info")


async def show_all_command(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with all records in database."""
    chat_id = update.effective_chat.id
    user_table = UserTable(chat_id)
    records = user_table.show_all()
    count = records.count()

    if count:
        persons = create_persons_info_list(records.all())
        message = [f'🗂 Список людей в базе ({count}):']
        message.extend(persons)
    else:
        message = ['В базе данных нет записей! '
                   'Может добавите кого-нибудь? /add']
    logging.info(f'Send message about all records '
                 f'to {_get_user_info(update)}. Message: {message}')
    await update.message.reply_text('\n'.join(message),
                                    reply_markup=MAIN_BUTTONS)


async def today_birthdays_command(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with today birthdays."""
    chat_id = update.effective_chat.id
    user_table = UserTable(chat_id)
    records = user_table.today_birthdays()
    message = check_today_birthdays(records)
    if message is None:
        message = ['Сегодня ни у кого нет дня рождения :(']
    logging.info(f'Send message about today birthdays '
                 f'to {_get_user_info(update)}. Message: {message}')
    await update.message.reply_text('\n'.join(message),
                                    reply_markup=MAIN_BUTTONS)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # await update.message.reply_text(update.message.text)
    # await update.message.reply_text(context.user_data,
    #                                 reply_markup=MAIN_BUTTONS)
    await update.message.reply_text(
        "Я знаю только команды и не умею общаться "
        ":( Узнай команды в /help и я смогу тебе помочь.",
        reply_markup=MAIN_BUTTONS)


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(add_conv_handler)
    application.add_handler(delete_conv_handler)
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("show_all", show_all_command))
    application.add_handler(CommandHandler("today", today_birthdays_command))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()


if __name__ == "__main__":
    configure_logging('birthdaygram.log')
    main()
