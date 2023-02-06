import datetime as dt

from exceptions import BirthDateError


def birth_date_validator(birth: str) -> str:
    """Validate is birthdate specified correct."""
    try:
        birth_date = dt.datetime.strptime(birth, '%d.%m.%Y')
    except ValueError:
        raise BirthDateError('Дата рождения указана некорректно! Укажите заново.')
    return birth_date.strftime('%Y-%m-%d')
