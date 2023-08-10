import logging

from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters,)

from alchemy_actions import UserTable
from utils import (
    create_persons_info_list,
    get_today_birthdays_message,
    get_next_interval_birthdays_message,
    get_user_info
)
from tg_handlers import (
    add_conv_handler,
    delete_conv_handler,
    MAIN_BUTTONS,
    ALL_BTN,
    TODAY_BTN,
    WEEK_BTN,
    MONTH_BTN,
    HELP_BTN
)
from constants import TOKEN, BIRTHDAYGRAM_LOG_NAME
from configs import configure_logging


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start or /help is issued."""
    if update.message.text == '/start':
        logging.info(f'Someone starts bot: {get_user_info(update)}')

    await update.message.reply_html(
        f"👋 Привет {update.effective_user.mention_html()}!\n\n"
        f"<b>Команды бота</b>\n"
        f"/add - добавить человека в список\n"
        f"/delete - удалить человека из списка\n"
        f"/show_all - список дней рождений\n"
        f"/today - у кого сегодня день рождения\n"
        f"/week - у кого есть дни рождения в течение 7 дней\n"
        f"/month - у кого есть дни рождения в течение 30 дней\n\n"
        f"/menu - открыть меню\n\n"
        f"Когда у кого-то из списка будет день рождения, "
        f"я сообщу тебе об этом.",
        reply_markup=MAIN_BUTTONS
    )


async def show_all_command(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with all records in database."""
    user_table = UserTable(update.effective_chat.id)
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
                 f'to {get_user_info(update)}. Message: {message}')
    await update.message.reply_text('\n'.join(message),
                                    reply_markup=MAIN_BUTTONS)


async def today_birthdays_command(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with today birthdays."""
    user_table = UserTable(update.effective_chat.id)
    records = user_table.today_birthdays()
    message = get_today_birthdays_message(records)
    if message is None:
        message = ['Сегодня ни у кого нет дня рождения :(']
    logging.info(f'Send message about today birthdays '
                 f'to {get_user_info(update)}. Message: {message}')
    await update.message.reply_text('\n'.join(message),
                                    reply_markup=MAIN_BUTTONS)


async def send_next_birthdays_message(update, interval) -> None:
    """Gets DB records for selected interval,
    sends telegram message for user about birthdays in this interval."""
    user_table = UserTable(update.effective_chat.id)
    records = user_table.next_days_interval_birthdays(interval)
    message = get_next_interval_birthdays_message(records, interval)
    if message is None:
        message = [f'В течение {interval} дней ни у кого нет дней рождения.']

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


async def show_menu(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text(
        'Используйте меню внизу экрана для взаимодействия со мной\n\n ⬇️',
        reply_markup=MAIN_BUTTONS
    )


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
    application.add_handler(MessageHandler(
        filters.Regex(HELP_BTN)
        | filters.Regex("/start")
        | filters.Regex("/help"),
        start
    ))
    application.add_handler(MessageHandler(
        filters.Regex(ALL_BTN) | filters.Regex("/show_all"),
        show_all_command
    ))
    application.add_handler(MessageHandler(
        filters.Regex(TODAY_BTN) | filters.Regex("/today"),
        today_birthdays_command
    ))
    application.add_handler(MessageHandler(
        filters.Regex(WEEK_BTN) | filters.Regex("/week"),
        next_week_birthday_command
    ))
    application.add_handler(MessageHandler(
        filters.Regex(MONTH_BTN) | filters.Regex("/month"),
        next_month_birthdays_command
    ))

    application.add_handler(CommandHandler('menu', show_menu))

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()


if __name__ == "__main__":
    configure_logging(BIRTHDAYGRAM_LOG_NAME)
    main()
