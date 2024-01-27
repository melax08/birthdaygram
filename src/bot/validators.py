import datetime as dt

import pytz

from bot.database import UserTable

from .constants.constants import BOT_TIMEZONE, DATE_FORMAT, FULL_NAME_MAX_LEN
from .constants.messages import (
    INCORRECT_BIRTHDATE,
    NAME_ALREADY_EXISTS,
    TOO_LONG_NAME,
    UNBORN_PERSON,
)
from .exceptions import BirthDateError, FullNameError


def birth_date_validator(birth: str) -> dt.date:
    """Validate is birthdate specified correct.
    Returns `datetime.date` object of this date."""
    try:
        birth_date = dt.datetime.strptime(birth, DATE_FORMAT).date()
    except ValueError:
        raise BirthDateError(INCORRECT_BIRTHDATE)

    if birth_date > dt.datetime.now(pytz.timezone(BOT_TIMEZONE)).date():
        raise BirthDateError(UNBORN_PERSON)

    return birth_date


async def full_name_validator(full_name: str, user_table: UserTable) -> None:
    """
    Validate full name.
    Full name len must be > than `FULL_NAME_MAX_LEN` and must be unique.
    """
    if len(full_name) > FULL_NAME_MAX_LEN:
        raise FullNameError(TOO_LONG_NAME.format(len(full_name), FULL_NAME_MAX_LEN))

    user_in_db = await user_table.select_person(full_name)
    if user_in_db is not None:
        raise FullNameError(NAME_ALREADY_EXISTS)
