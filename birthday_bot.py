import sys
import os
import datetime as dt

from dotenv import load_dotenv
from telegram import Bot

from db_actions import Database

load_dotenv()

TOKEN = os.getenv('TOKEN')
TELEGRAM_ID = os.getenv('TELEGRAM_ID')


def send_message(message) -> None:
    """Send telegram message about today birthdays."""
    bot = Bot(token=TOKEN)
    bot.send_message(TELEGRAM_ID, message)


def today_birthdays_message_send(today_birthdays: list) -> None:
    """Send telegram message about today birthdays."""
    if today_birthdays:
        strings = []
        current_year = dt.datetime.now().year
        if len(today_birthdays) == 1:
            strings.append('⚡️ Сегодня день рождения у:\n')
        else:
            strings.append('⚡️ Сегодня дни рождения у:\n')
        for name, birthdate in today_birthdays:
            birthdate = dt.datetime.strptime(birthdate, '%Y-%m-%d')
            age = current_year - birthdate.year
            strings.append(f'🎂 {name}, исполнилось: '
                           f'{age} ({birthdate:%d.%m.%Y})\n')
        send_message(' '.join(strings))


def main() -> None:
    """Main function."""
    database = Database()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'create_database':
            database.create_table()
        elif sys.argv[1] == 'add':
            name = sys.argv[2]
            birthdate = sys.argv[3]
            database.new_record(name, birthdate)
        else:
            print(f'Wrong argument: {sys.argv[1]}')
    else:
        today_birthdays_message_send(database.today_birthdays())


if __name__ == '__main__':
    main()
