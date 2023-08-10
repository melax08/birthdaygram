"""
Cron task for check today and next birthdays for all users.
"""
import asyncio
import logging

from alchemy_actions import CheckTable, UserTable
from utils import get_today_birthdays_message, send_message
from configs import configure_logging


def get_tables() -> list:
    """Connects to database and gets a list of tables that are chat_id."""
    database = CheckTable()
    return database.select_tables()


async def tables_processing(tables: list) -> None:
    """Checks every table for today birthdays,
    sends a message to the user if any."""
    for chat_id in tables:
        user = UserTable(chat_id)
        user_today_birthdays = user.today_birthdays()
        message = get_today_birthdays_message(user_today_birthdays)
        if message is not None:
            logging.info(f'User: {chat_id} has today birthdays. '
                         f'Sending a message.')
            await send_message('\n'.join(message), chat_id)


async def main():
    """Main coroutine."""
    tables = get_tables()
    await tables_processing(tables)


if __name__ == '__main__':
    configure_logging('cron.log')
    logging.info('Cron started!')
    asyncio.run(main())
    logging.info('Cron finished.')
