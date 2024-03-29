import datetime as dt

from telegram import Bot, Update

from .constants.constants import DATE_FORMAT, TOKEN
from .constants.messages import PERSON_INFO


async def send_message(message: str, chat_id: str) -> None:
    """Sends the specified telegram message to the specified user."""
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id, message)


def birthdate_processing(birthdate: dt) -> tuple:
    """Processes the date of birth from the database
    and returns a human-readable date and current age."""
    now = dt.datetime.now()
    age = now.year - birthdate.year
    if birthdate.month == now.month:
        if birthdate.day > now.day:
            age -= 1
    elif birthdate.month > now.month:
        age -= 1
    return birthdate.strftime(DATE_FORMAT), age


def create_persons_info_list(data: list) -> list:
    """Creates a message with information about selected person(s)."""
    message = []
    for record in data:
        birthdate, age = birthdate_processing(record.birth_date)
        message.append(PERSON_INFO.format(record.full_name, age, birthdate))
    return message


def get_user_info(update: Update) -> str:
    """Creates a string with information about the current telegram user."""
    user = update.effective_user
    return f"{user.username}, {user.first_name} {user.last_name}, {user.id}"
