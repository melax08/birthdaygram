"""
Cron task for check today and next birthdays for all users.
"""
import asyncio
import logging

from bot.database import CheckTable
from bot.utils import send_message
from configs import configure_logging
from bot.handlers.services import today_birthdays, next_week_birthdays
from bot.exceptions import EmptyQuery


def get_tables() -> list:
    """Connects to database and gets a list of tables that are chat_id."""
    database = CheckTable()
    return database.select_tables()


async def tables_processing(tables: list) -> None:
    """Checks every table for today birthdays,
    sends a message to the user if any."""
    for chat_id in tables:
        try:
            today_message = today_birthdays(chat_id)
            logging.info(f'User: {chat_id} has today birthdays. '
                         f'Sending a message.')
            await send_message('\n'.join(today_message), chat_id)
        except EmptyQuery:
            pass

        try:
            week_message = next_week_birthdays(chat_id)
            logging.info(f'User: {chat_id} has next week birthdays. '
                         f'Sending a message.')
            await send_message('\n'.join(week_message), chat_id)
        except EmptyQuery:
            pass


async def main():
    """Main coroutine."""
    tables = get_tables()
    await tables_processing(tables)


if __name__ == '__main__':
    configure_logging('cron.log')
    logging.info('Cron started!')
    asyncio.run(main())
    logging.info('Cron finished.')
