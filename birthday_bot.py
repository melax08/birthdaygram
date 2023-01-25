import sqlite3
import sys
import os
import datetime as dt

from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv('TOKEN')
TELEGRAM_ID = os.getenv('TELEGRAM_ID')


def db_actions(func):
    """Decorator for quick database actions."""
    def db_processing(*args, **kwargs):
        """Create db connect, cursor, using it to process some action."""
        connect = sqlite3.connect('birthdays.db')
        cursor = connect.cursor()
        result = func(*args, cursor, **kwargs)
        connect.commit()
        connect.close()
        return result
    return db_processing


@db_actions
def create_table(cursor) -> None:
    """Create database and birthday table."""
    try:
        cursor.execute("""CREATE TABLE birthdays(
            full_name VARCHAR(255), 
            birth_date DATE
        )""")
        print('Database was succesfuly created!')
    except sqlite3.OperationalError as error:
        print(f'Error! {error}')


@db_actions
def create_new_record(name: str, birthday: str, cursor) -> None:
    """Create new birthday record."""
    cursor.execute(
        f"INSERT INTO birthdays (full_name, birth_date) VALUES ('{name}', '{birthday}');")


@db_actions
def select_today_birthdays(cursor) -> list:
    """Select today birthdays from database."""
    return cursor.execute(f"SELECT * FROM birthdays WHERE strftime('%m-%d', birth_date) = strftime('%m-%d',date('now', 'localtime'));").fetchall()


def send_message(message) -> None:
    """Send telegram message about today birthdays."""
    bot = Bot(token=TOKEN)
    bot.send_message(TELEGRAM_ID, message)


def today_birthdays_message_send() -> None:
    """Send telegram message about today birthdays."""
    today_birthdays = select_today_birthdays()
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
    if len(sys.argv) > 1:
        if sys.argv[1] == 'create_database':
            create_table()
        elif sys.argv[1] == 'add':
            name = sys.argv[2]
            birthdate = sys.argv[3]
            create_new_record(name, birthdate)
        else:
            print(f'Wrong argument: {sys.argv[1]}')
    else:
        today_birthdays_message_send()


if __name__ == '__main__':
    main()
