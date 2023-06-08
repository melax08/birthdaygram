import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters,)

from alchemy_actions import UserTable
from birthday_bot import create_persons_info_list, check_today_birthdays
from tg_handlers import add_conv_handler, delete_conv_handler, MAIN_BUTTONS



load_dotenv()

TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


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

    await update.message.reply_text('\n'.join(message))


async def today_birthdays_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_table = UserTable(chat_id)
    records = user_table.today_birthdays()
    message = check_today_birthdays(records)
    if message is None:
        message = ['Сегодня ни у кого нет дня рождения :(']
    await update.message.reply_text('\n'.join(message))



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # await update.message.reply_text(update.message.text)
    await update.message.reply_text(context.user_data)


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(add_conv_handler)
    application.add_handler(delete_conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("show_all", show_all_command))
    application.add_handler(CommandHandler("today", today_birthdays_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()


if __name__ == "__main__":
    main()
