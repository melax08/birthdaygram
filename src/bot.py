import pytz

from telegram.ext import Application, Defaults

from bot.constants.constants import BIRTHDAYGRAM_LOG_NAME, TOKEN, BOT_TIMEZONE
from bot.handlers.add_handler import add_handler
from bot.handlers.birthday_handlers import (
    month_handler,
    show_all_handler,
    today_handler,
    week_handler
)
from bot.handlers.delete_handler import delete_handler
from bot.handlers.main_handlers import (
    menu_handler,
    start_handler,
    text_handler
)
from bot.handlers.scheduler import set_scheduler
from logger import configure_logging


def start_bot() -> None:
    """Build bot application, collect handlers and start polling."""
    defaults = Defaults(tzinfo=pytz.timezone(BOT_TIMEZONE))
    application = Application.builder().token(TOKEN).defaults(defaults).build()
    set_scheduler(application.job_queue)
    application.add_handlers(
        (
            add_handler,
            delete_handler,
            start_handler,
            show_all_handler,
            today_handler,
            week_handler,
            month_handler,
            menu_handler,
            text_handler,
        )
    )
    application.run_polling()


if __name__ == "__main__":
    configure_logging(BIRTHDAYGRAM_LOG_NAME)
    start_bot()
