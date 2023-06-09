"""
Cron task for check today and next birthdays for all users.
"""
import asyncio

from alchemy_actions import CheckTable, UserTable
from birthday_bot import check_today_birthdays, send_message


def get_tables() -> list:
    """Connect to database and get list of tables which chat_id."""
    database = CheckTable()
    return database.select_tables()


async def tables_processing(tables: list) -> None:
    """Check every table for today birthdays, send message to user if any."""
    for chat_id in tables:
        user = UserTable(chat_id)
        user_today_birthdays = user.today_birthdays()
        message = check_today_birthdays(user_today_birthdays)
        if message is not None:
            await send_message('\n'.join(message), chat_id)


async def main():
    """Main coroutine."""
    tables = get_tables()
    await tables_processing(tables)


if __name__ == '__main__':
    asyncio.run(main())
