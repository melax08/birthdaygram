import datetime as dt

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import Session, declared_attr, declarative_base
from sqlalchemy.sql.expression import extract

from constants import FULL_NAME_MAX_LEN, SQLITE_DB_NAME


class PreBase:
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
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.session, self.user_table = self.__get_session_and_table()

    def __get_session_and_table(self):
        class User(Base):
            chat_id = self.chat_id

        engine = create_engine(f'sqlite:///{SQLITE_DB_NAME}', echo=True)
        Base.metadata.create_all(engine)
        session = Session(engine)
        return session, User

    def show_all(self):
        return self.session.query(self.user_table)

    def add_person(self, name: str, birthdate: dt) -> None:
        new_person = self.user_table(full_name=name, birth_date=birthdate)
        self.session.add(new_person)
        self.session.commit()

    def select_person(self, name):
        return self.session.query(self.user_table).filter(
            self.user_table.full_name == name).first()

    def delete_person(self, person):
        self.session.delete(person)
        self.session.commit()

    def today_birthdays(self):
        today = dt.date.today()
        return self.session.query(self.user_table).filter(
            extract("month", self.user_table.birth_date == today.month),
            extract("day", self.user_table.birth_date) == today.day).all()

    def __del__(self):
        self.session.close()


if __name__ == "__main__":
    table = UserTable(159956275)
    print()
