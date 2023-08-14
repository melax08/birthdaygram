from telegram.ext import Application

from bot.constants.constants import BIRTHDAYGRAM_LOG_NAME, TOKEN
from bot.handlers.add_handler import add_handler
from bot.handlers.birthday_handlers import (month_handler, show_all_handler,
                                            today_handler, week_handler)
from bot.handlers.delete_handler import delete_handler
from bot.handlers.main_handlers import (menu_handler, start_handler,
                                        text_handler)
from configs import configure_logging


def start_bot() -> None:
    """Build bot application, collect handlers and start polling."""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(add_handler)
    application.add_handler(delete_handler)
    application.add_handler(start_handler)
    application.add_handler(show_all_handler)
    application.add_handler(today_handler)
    application.add_handler(week_handler)
    application.add_handler(month_handler)
    application.add_handler(menu_handler)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == "__main__":
    configure_logging(BIRTHDAYGRAM_LOG_NAME)
    start_bot()
