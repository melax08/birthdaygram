from typing import List

from bot.database import UserTable
from bot.exceptions import EmptyQuery
from bot.utils import create_persons_info_list, birthdate_processing
from bot.constants.messages import (
    EMPTY_TABLE_MESSAGE,
    NO_BIRTHDAYS_TODAY,
    TODAY_BIRTHDAYS_LABEL,
    PERSON_BIRTHDAY,
    LIST_PERSONS_LABEL,
    NEXT_WEEK_BIRTHDAY_LABEL,
    PERSON_NEXT_BIRTHDAY,
    INTERVAL_NO_BIRTHDAYS,
    INTERVAL_BIRTHDAY_LABEL
)


def show_all(chat_id: int) -> List[str]:
    """Logic of `show all` button."""
    user_table = UserTable(chat_id)
    records = user_table.show_all()
    count = len(records)

    if not count:
        raise EmptyQuery(EMPTY_TABLE_MESSAGE)

    persons = create_persons_info_list(records)
    message = [LIST_PERSONS_LABEL.format(count)]
    message.extend(persons)
    return message


def today_birthdays(chat_id: int) -> List[str]:
    """Logic of showing today birthdays functional."""
    user_table = UserTable(chat_id)
    records = user_table.today_birthdays()

    if not len(records):
        raise EmptyQuery(NO_BIRTHDAYS_TODAY)

    message = [TODAY_BIRTHDAYS_LABEL]
    for record in records:
        birthdate, age = birthdate_processing(record.birth_date)
        message.append(
            PERSON_BIRTHDAY.format(record.full_name, age, birthdate)
        )

    return message


def next_week_birthdays(chat_id: int) -> List[str]:
    """Logic of showing birthdays in 7 days."""
    user_table = UserTable(chat_id)
    records = user_table.next_week_birthdays()

    if not len(records):
        raise EmptyQuery

    message = [NEXT_WEEK_BIRTHDAY_LABEL]
    for record in records:
        birthdate, age = birthdate_processing(record.birth_date)
        message.append(
            PERSON_NEXT_BIRTHDAY.format(record.full_name, age + 1, birthdate)
        )

    return message


def next_birthdays(chat_id: int, interval: int) -> List[str]:
    """Logic of showing birthdays in interval from now to `interval`."""
    user_table = UserTable(chat_id)
    records = user_table.next_days_interval_birthdays(interval)

    if not len(records):
        raise EmptyQuery(INTERVAL_NO_BIRTHDAYS.format(interval))

    message = [INTERVAL_BIRTHDAY_LABEL.format(interval)]

    for record in records:
        birthdate, age = birthdate_processing(record.birth_date)
        message.append(
            PERSON_NEXT_BIRTHDAY.format(record.full_name, age + 1, birthdate)
        )

    return message
