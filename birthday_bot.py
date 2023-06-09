import datetime as dt
from typing import Optional

from telegram import Bot

from constants import TOKEN


async def send_message(message: str, chat_id: str) -> None:
    """Send telegram message."""
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id, message)


def birthdate_processing(birthdate: dt) -> tuple:
    """Processes the date of birth from the
    database and returns a human-readable date and current age."""
    age = dt.datetime.now().year - birthdate.year
    return f'{birthdate:%d.%m.%Y}', age


def check_today_birthdays(records: list) -> Optional[list]:
    """Check today birthdays query, return message if any birthday."""
    message = None
    if len(records) > 0:
        message = ['⚡️ Сегодня день рождения у:']
        for record in records:
            birthdate, age = birthdate_processing(record.birth_date)
            message.append(
                f'🎂 {record.full_name}, исполнилось: {age} ({birthdate})')
    return message


def create_persons_info_list(data: list) -> list:
    """Create message with information about selected person(s)."""
    message = []
    for record in data:
        birthdate, age = birthdate_processing(record.birth_date)
        message.append(f'{record.full_name}, возраст: {age}, {birthdate}')
    return message
