import os
import datetime as dt

from sqlalchemy import create_engine, Column, Integer, String, Date, inspect
from sqlalchemy.orm import Session, declared_attr, declarative_base
from sqlalchemy.sql.expression import extract

from constants import FULL_NAME_MAX_LEN, SQLITE_DB_NAME


if os.getenv('LOCAL', default=0):
    sql_settings = f'sqlite:///{SQLITE_DB_NAME}'
else:
    db_user = os.getenv("POSTGRES_USER", default='birthdaygram')
    db_password = os.getenv("POSTGRES_PASSWORD", default='123456')
    db_host = os.getenv("DB_HOST", default='db')
    db_port = os.getenv("DB_PORT", default=5432)
    db_name = os.getenv("DB_NAME", default='birthdaygram')
    sql_settings = (
        f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    )


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

        self.engine = create_engine(sql_settings, echo=False)
        Base.metadata.create_all(self.engine)
        session = Session(self.engine)
        return session, User

    def show_all(self):
        """Makes DB query to get all user records in table."""
        return self.session.query(self.user_table)

    def add_person(self, name: str, birthdate: dt) -> None:
        """Makes DB query to add new record to user table."""
        new_person = self.user_table(full_name=name, birth_date=birthdate)
        self.session.add(new_person)
        self.session.commit()

    def select_person(self, name):
        """Selects record from DB with specified full_name."""
        return self.session.query(self.user_table).filter(
            self.user_table.full_name == name).first()

    def delete_person(self, person):
        """Deletes record from DB with specified person."""
        self.session.delete(person)
        self.session.commit()

    def today_birthdays(self):
        """Makes DB query to get all user records with today birthdays."""
        today = dt.date.today()
        return self.session.query(self.user_table).filter(
            extract("month", self.user_table.birth_date == today.month),
            extract("day", self.user_table.birth_date) == today.day).all()

    def __del__(self):
        self.session.close()


class CheckTable:
    """Manages infrastructure DB tasks."""
    def __init__(self):
        self.__connect()

    def __connect(self):
        self.engine = create_engine(sql_settings, echo=False)

    def select_tables(self):
        """Makes DB query to get all DB tables names."""
        insp = inspect(self.engine)
        return insp.get_table_names()


if __name__ == "__main__":
    table = UserTable(159956275)
    print()
