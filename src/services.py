from typing import List

from database import UserTable
from exceptions import EmptyQuery
from utils import create_persons_info_list, birthdate_processing


def show_all(chat_id: int) -> List[str]:
    """Logic of `show all` button."""
    user_table = UserTable(chat_id)
    records = user_table.show_all()
    count = len(records)

    if not count:
        raise EmptyQuery('В базе данных нет записей! '
                         'Может добавите кого-нибудь? /add')

    persons = create_persons_info_list(records)
    message = [f'🗂 Список людей в базе ({count}):']
    message.extend(persons)
    return message


def today_birthdays(chat_id: int) -> List[str]:
    """Logic of showing today birthdays functional."""
    user_table = UserTable(chat_id)
    records = user_table.today_birthdays()

    if not len(records):
        raise EmptyQuery('Сегодня ни у кого нет дня рождения :(')

    message = ['⚡️ Сегодня день рождения у:']
    for record in records:
        birthdate, age = birthdate_processing(record.birth_date)
        message.append(
            f'🎂 {record.full_name}, исполнилось: {age} ({birthdate})')

    return message


def next_week_birthdays(chat_id: int) -> List[str]:
    user_table = UserTable(chat_id)
    records = user_table.next_week_birthdays()

    if not len(records):
        raise EmptyQuery

    message = ['‼️ Ровно через неделю день рождения у:']
    for record in records:
        birthdate, age = birthdate_processing(record.birth_date)
        message.append(
            f'{record.full_name}, исполнится: {age + 1} ({birthdate})'
        )

    return message


def next_birthdays(chat_id: int, interval: int) -> List[str]:
    """Logic of showing birthdays in interval from now to `interval`."""
    user_table = UserTable(chat_id)
    records = user_table.next_days_interval_birthdays(interval)

    if not len(records):
        raise EmptyQuery(
            f'В течение {interval} дней ни у кого нет дней рождения.'
        )

    message = [
        f'❕ В течение следующих {interval} дней есть дни рождения у:\n'
    ]

    for record in records:
        birthdate, age = birthdate_processing(record.birth_date)
        message.append(
            f'{record.full_name}, исполнится: {age + 1} ({birthdate})'
        )

    return message
