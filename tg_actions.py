import logging
import os

from dotenv import load_dotenv
from telegram import ForceReply, Update, ReplyKeyboardMarkup
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters, ConversationHandler)

from db_actions import Database
from birthday_bot import all_records
from validators import birth_date_validator
from exceptions import BirthDateError


load_dotenv()

TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

FULL_NAME, BIRTHDATE, CONFIRMATION = range(3)
MAIN_BUTTONS = ReplyKeyboardMarkup([
        ['/add', '/show_all']
    ], resize_keyboard=True, input_field_placeholder='Выберите действия:')
YES_NO_BUTTONS = buttons = ReplyKeyboardMarkup([['Да', 'Нет']])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=MAIN_BUTTONS
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("There is some help info")


async def show_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with all records in database."""
    db = Database()
    records = db.show_all_records()
    message = all_records(records)
    await update.message.reply_text(message)


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Напишите полное имя человека, для отмены /cancel')
    return FULL_NAME


async def _full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["full_name"] = update.message.text
    await update.message.reply_text('Напишите дату рождения человека в формате dd.mm.yyyy, для отмены /cancel')
    return BIRTHDATE


async def _birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    birth_date = update.message.text
    try:
        birth_date_db = birth_date_validator(birth_date)
    except BirthDateError as error:
        await update.message.reply_text(str(error))
        return BIRTHDATE
    context.user_data["birth_date"] = birth_date_db
    await update.message.reply_text(f'Вы добавили: {context.user_data.get("full_name")}, дата рождения: {birth_date}. Все верно?', reply_markup=YES_NO_BUTTONS)
    return CONFIRMATION


async def _confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text
    if answer == 'Нет':
        await update.message.reply_text('В таком случае, заполните все сначала. Напишите имя человека.')
        return FULL_NAME
    elif answer == 'Да':
        db = Database()
        db.new_record(context.user_data.get("full_name"), context.user_data.get("birth_date"))
        del context.user_data["full_name"]
        del context.user_data["birth_date"]
        await update.message.reply_text('Успешно!', reply_markup=MAIN_BUTTONS)
        return ConversationHandler.END
    else:
        await update.message.reply_text('Ответьте, Да или Нет.', reply_markup=YES_NO_BUTTONS)
        return CONFIRMATION


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    del context.user_data["full_name"]
    del context.user_data["birth_date"]
    await update.message.reply_text(
        "Действие отменено."
    )
    return ConversationHandler.END


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("show_all", show_all_command))

    add_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add_command)],
        states={
            FULL_NAME: [MessageHandler(filters.TEXT, _full_name)],
            BIRTHDATE: [MessageHandler(filters.TEXT, _birth_date)],
            CONFIRMATION: [MessageHandler(filters.TEXT, _confirmation)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(add_handler)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()


if __name__ == "__main__":
    main()
