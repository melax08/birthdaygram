import datetime as dt

from exceptions import BirthDateError, FullNameError

FULL_NAME_MAX_LEN = 50


def birth_date_validator(birth: str) -> str:
    """Validate is birthdate specified correct."""
    try:
        birth_date = dt.datetime.strptime(birth, '%d.%m.%Y')
    except ValueError:
        raise BirthDateError('❗ Дата рождения указана некорректно! Укажите заново.')
    return birth_date.strftime('%Y-%m-%d')


def full_name_validator(full_name: str) -> None:
    """Validate full name."""
    if len(full_name) > FULL_NAME_MAX_LEN:
        raise FullNameError(f'❗ Указанное имя слишком длинное. Вы указали имя длинной: {len(full_name)} символов, максимальная длина: {FULL_NAME_MAX_LEN}. Укажите имя заново.')
