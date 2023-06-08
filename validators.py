import datetime as dt

from exceptions import BirthDateError, FullNameError
from constants import FULL_NAME_MAX_LEN


def birth_date_validator(birth: str) -> dt:
    """Validate is birthdate specified correct.
    Returns datetime object of this date."""
    try:
        birth_date = dt.datetime.strptime(birth, '%d.%m.%Y')
    except ValueError:
        raise BirthDateError(
            '❗ Дата рождения указана некорректно! Укажите заново.')
    return birth_date


def full_name_validator(full_name: str) -> None:
    """Validate full name."""
    if len(full_name) > FULL_NAME_MAX_LEN:
        raise FullNameError(
            f'❗ Указанное имя слишком длинное. '
            f'Вы указали имя длинной: {len(full_name)} символов, '
            f'максимальная длина: {FULL_NAME_MAX_LEN}. Укажите имя заново.')
