import datetime as dt

from sqlalchemy import (create_engine, Column, Integer, String, Date, inspect,
                        func, select, Interval, and_)
from sqlalchemy.orm import Session, declared_attr, declarative_base
from sqlalchemy.sql.expression import extract

from constants import FULL_NAME_MAX_LEN, SQL_SETTINGS, ECHO


class PreBase:
    """Base class for user model. Name of the table is user telegram id,
    every user has its own table."""
    chat_id = 'default_table'

    @declared_attr
    def __tablename__(cls):
        return cls.chat_id

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    full_name = Column(String(FULL_NAME_MAX_LEN))
    birth_date = Column(Date)

    def __repr__(self):
        return f'{self.full_name} - {self.birth_date}'


Base = declarative_base(cls=PreBase)


class UserTable:
    """Class for handle user table DB queries."""
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.session, self.user_table = self.__get_session_and_table()

    def __get_session_and_table(self):
        """Creates DB session and current user model."""
        class User(Base):
            chat_id = self.chat_id

        self.engine = create_engine(SQL_SETTINGS, echo=ECHO)
        Base.metadata.create_all(self.engine)
        session = Session(self.engine)
        return session, User

    def show_all(self):
        """Makes DB query to get all user records in table."""
        return self.session.execute(
            select(self.user_table).order_by(
                extract("month", self.user_table.birth_date),
                extract("day", self.user_table.birth_date)
            )
        ).scalars().all()

    def add_person(self, name: str, birthdate: dt) -> None:
        """Makes DB query to add new record to user table."""
        new_person = self.user_table(full_name=name, birth_date=birthdate)
        self.session.add(new_person)
        self.session.commit()

    def select_person(self, name):
        """Selects the record from DB with specified full_name."""
        return self.session.execute(
            select(self.user_table).where(
                self.user_table.full_name == name
            )
        ).scalars().first()

    def delete_person(self, person):
        """Deletes the record from DB with specified person."""
        self.session.delete(person)
        self.session.commit()

    def _birthdays_in_date(self, date: dt):
        """Selects persons with birthday in specified date."""
        return self.session.execute(
            select(self.user_table).where(and_(
                func.cast(extract("month", self.user_table.birth_date),
                          Integer) == date.month),
                func.cast(extract("day", self.user_table.birth_date),
                          Integer) == date.day)
        ).scalars().all()

    def today_birthdays(self):
        """Makes DB query to get all user records with today birthdays."""
        return self._birthdays_in_date(dt.date.today())

    def next_week_birthdays(self):
        """Makes DB query to get all user records with birthdays in 7 days."""
        return self._birthdays_in_date(dt.date.today() + dt.timedelta(days=7))


    @staticmethod
    def age_years_at(sa_col, next_days: int = 0):
        """
        Generates a postgresql specific statement to return 'age' (in years)
        from the provided field either today (next_days == 0)
        or with the `next_days` offset.
        """
        statement = func.age(
            (sa_col - func.cast(dt.timedelta(next_days), Interval))
            if next_days != 0
            else sa_col
        )
        return func.date_part("year", statement)

    def has_birthday_next_days(self, sa_col, next_days: int = 0):
        """
        Sqlalchemy expression to indicate that
        a sa_col (such as`User.birth_date`)
        has anniversary within next `next_days` days.

        It is implemented by checking if the 'age' of the person (in years)
        has changed between today and the `next_days` date.
        """
        return self.age_years_at(sa_col, next_days) > self.age_years_at(sa_col)

    def next_days_interval_birthdays(self, days):
        """Selects all birthdays from the user table
        with anniversary in specified next days."""
        return self.session.execute(
            select(
                self.user_table
            ).where(
                self.has_birthday_next_days(self.user_table.birth_date, days))
        ).scalars().all()

    def __del__(self):
        self.session.close()


class CheckTable:
    """Manages infrastructure DB tasks."""
    def __init__(self):
        self.__connect()

    def __connect(self):
        self.engine = create_engine(SQL_SETTINGS, echo=ECHO)

    def select_tables(self):
        """Makes DB query to get all DB tables names."""
        insp = inspect(self.engine)
        return insp.get_table_names()


if __name__ == "__main__":
    table = UserTable(159956275)
    print()
