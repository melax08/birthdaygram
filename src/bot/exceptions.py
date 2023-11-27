class BirthDateError(Exception):
    """Raises if something wrong with passed birthdate."""

    pass


class FullNameError(Exception):
    """Raises if something wrong with passed full name."""

    pass


class EmptyQuery(Exception):
    """Raises if selected query from database is empty."""

    pass
