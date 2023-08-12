import datetime as dt

from telegram import Bot, Update

from constants import TOKEN


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
    return f'{birthdate:%d.%m.%Y}', age


def create_persons_info_list(data: list) -> list:
    """Creates a message with information about selected person(s)."""
    message = []
    for record in data:
        birthdate, age = birthdate_processing(record.birth_date)
        message.append(f'{record.full_name}, возраст: {age}, {birthdate}')
    return message


def get_user_info(update: Update) -> str:
    """Creates a string with information about the current telegram user."""
    info = update.message
    return (f'{info.chat.username}, {info.chat.first_name} '
            f'{info.chat.last_name}, {update.effective_user.id}')
