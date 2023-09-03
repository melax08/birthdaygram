import datetime as dt

from .constants.constants import DATE_FORMAT, FULL_NAME_MAX_LEN
from .constants.messages import (INCORRECT_BIRTHDATE, TOO_LONG_NAME,
                                 UNBORN_PERSON, NAME_ALREADY_EXISTS)
from .exceptions import BirthDateError, FullNameError
from bot.database import UserTable


def birth_date_validator(birth: str) -> dt:
    """Validate is birthdate specified correct.
    Returns datetime object of this date."""
    try:
        birth_date = dt.datetime.strptime(birth, DATE_FORMAT)
    except ValueError:
        raise BirthDateError(INCORRECT_BIRTHDATE)
    now = dt.datetime.now()
    if ((birth_date.year > now.year)
            or (birth_date.year == now.year and birth_date.month > now.month)
            or (birth_date.year == now.year and birth_date.month == now.month
                and birth_date.day > now.day)):
        raise BirthDateError(UNBORN_PERSON)
    return birth_date


def full_name_validator(full_name: str, user_table: UserTable) -> None:
    """
    Validate full name.
    Full name len must be > than `FULL_NAME_MAX_LEN` and must be unique.
    """
    if len(full_name) > FULL_NAME_MAX_LEN:
        raise FullNameError(
            TOO_LONG_NAME.format(len(full_name), FULL_NAME_MAX_LEN)
        )

    user_in_db = user_table.select_person(full_name)
    if user_in_db is not None:
        raise FullNameError(NAME_ALREADY_EXISTS)
