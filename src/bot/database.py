import datetime as dt
from contextlib import asynccontextmanager

from sqlalchemy import (
    Column,
    Date,
    Integer,
    Interval,
    String,
    and_,
    func,
    inspect,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from sqlalchemy.sql.expression import extract

from .constants.constants import ECHO, FULL_NAME_MAX_LEN, SQL_SETTINGS


class PreBase:
    """Base class for user model. Name of the table is user telegram id,
    every user has its own table."""

    chat_id = "default_table"

    @declared_attr
    def __tablename__(cls):
        return cls.chat_id

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    full_name = Column(String(FULL_NAME_MAX_LEN))
    birth_date = Column(Date)

    def __repr__(self):
        return f"{self.full_name} - {self.birth_date}"


Base = declarative_base(cls=PreBase)
engine = create_async_engine(SQL_SETTINGS, echo=ECHO)


class UserTable:
    """Class for handle user table DB queries."""

    def __init__(self, chat_id):
        self.chat_id = chat_id

    async def get_session_and_table(self) -> None:
        """Opens DB session and get current user model.
        If the user model doesn't exist, creates it."""

        class User(Base):
            chat_id = self.chat_id

        async def init_models():
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        await init_models()

        AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

        self.user_table = User
        self.session = AsyncSessionLocal

    @asynccontextmanager
    async def _get_async_session(self):
        """Open async SQLAlchemy session and close it after all actions."""
        async with self.session() as async_session:
            yield async_session

    async def show_all(self):
        """Makes DB query to get all user records in table."""
        async with self._get_async_session() as session:
            all_birthdays = await session.execute(
                select(self.user_table).order_by(
                    extract("month", self.user_table.birth_date),
                    extract("day", self.user_table.birth_date),
                )
            )

        return all_birthdays.scalars().all()

    async def add_person(self, name: str, birthdate: dt) -> None:
        """Makes DB query to add new record to user table."""
        async with self._get_async_session() as session:
            new_person = self.user_table(full_name=name, birth_date=birthdate)
            session.add(new_person)
            await session.commit()

    async def select_person(self, name):
        """Selects the record from DB with specified full_name."""
        async with self._get_async_session() as session:
            person = await session.execute(
                select(self.user_table).where(self.user_table.full_name == name)
            )

        return person.scalars().first()

    async def delete_person(self, person) -> None:
        """Deletes the record from DB with specified person."""
        async with self._get_async_session() as session:
            await session.delete(person)
            await session.commit()

    async def _birthdays_in_date(self, date: dt):
        """Selects persons with birthday in specified date."""
        async with self._get_async_session() as session:
            birthdays = await session.execute(
                select(self.user_table).where(
                    and_(
                        func.cast(extract("month", self.user_table.birth_date), Integer)
                        == date.month
                    ),
                    func.cast(extract("day", self.user_table.birth_date), Integer)
                    == date.day,
                )
            )

        return birthdays.scalars().all()

    async def today_birthdays(self):
        """Makes DB query to get all user records with today birthdays."""
        return await self._birthdays_in_date(dt.date.today())

    async def next_week_birthdays(self):
        """Makes DB query to get all user records with birthdays in 7 days."""
        return await self._birthdays_in_date(dt.date.today() + dt.timedelta(days=7))

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

    async def next_days_interval_birthdays(self, days):
        """Selects all birthdays from the user table
        with anniversary in specified next days."""
        async with self._get_async_session() as session:
            birthdays = await session.execute(
                select(self.user_table).where(
                    self.has_birthday_next_days(self.user_table.birth_date, days)
                )
            )

        return birthdays.scalars().all()

    @staticmethod
    async def get_table_names():
        """Makes DB query to get all database tables names."""
        async with engine.connect() as conn:
            tables = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_names()
            )
        return tables

    @classmethod
    async def get_user_table(cls, chat_id: int):
        """Create UserTable class by user telegram chat id to give access to
        the database queries."""
        user_table = cls(chat_id)
        await user_table.get_session_and_table()
        return user_table
