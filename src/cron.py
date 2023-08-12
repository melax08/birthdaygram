"""
Cron task for check today and next birthdays for all users.
"""
import asyncio
import logging

from alchemy_actions import CheckTable
from utils import send_message
from configs import configure_logging
from services import today_birthdays
from exceptions import EmptyQuery


def get_tables() -> list:
    """Connects to database and gets a list of tables that are chat_id."""
    database = CheckTable()
    return database.select_tables()


async def tables_processing(tables: list) -> None:
    """Checks every table for today birthdays,
    sends a message to the user if any."""
    for chat_id in tables:
        try:
            message = today_birthdays(chat_id)
            logging.info(f'User: {chat_id} has today birthdays. '
                         f'Sending a message.')
            await send_message('\n'.join(message), chat_id)
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
