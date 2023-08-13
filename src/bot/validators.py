import datetime as dt

from .constants.constants import FULL_NAME_MAX_LEN, DATE_FORMAT
from .constants.messages import (
    INCORRECT_BIRTHDATE,
    UNBORN_PERSON,
    TOO_LONG_NAME
)
from .exceptions import BirthDateError, FullNameError


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


def full_name_validator(full_name: str) -> None:
    """Validate full name."""
    if len(full_name) > FULL_NAME_MAX_LEN:
        raise FullNameError(
            TOO_LONG_NAME.format(len(full_name), FULL_NAME_MAX_LEN)
        )
