"""
Old class for local raw SQL use.
Before use, you need to implement protection
against SQL injection on user input.
"""

import sqlite3
import os

DB_NAME = 'birthdays.db'
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)
TABLE_NAME = 'birthdays'


class Database:
    def __init__(self):
        self.__connect = sqlite3.connect(DB_PATH)
        self.__cursor = self.__connect.cursor()

    def create_table(self) -> None:
        try:
            self.__cursor.execute(f"""CREATE TABLE {TABLE_NAME}(full_name VARCHAR(255), birth_date DATE)""")
            print('Database was successfully created!')
        except sqlite3.OperationalError as error:
            print(f'Error! {error}')

    def new_record(self, name: str, birthday: str) -> None:
        self.__cursor.execute(f"INSERT INTO {TABLE_NAME} (full_name, birth_date) VALUES ('{name}', '{birthday}');")
        self.__connect.commit()

    def today_birthdays(self) -> list:
        return self.__cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE strftime('%m-%d', birth_date) = strftime('%m-%d',date('now', 'localtime'));").fetchall()

    def delete(self, name: str) -> None:
        self.__cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE full_name='{name}'")
        self.__connect.commit()

    def select(self, name: str):
        return self.__cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE full_name='{name}';").fetchall()

    def show_all_records(self) -> list:
        return self.__cursor.execute(f"SELECT * FROM {TABLE_NAME}").fetchall()

    def count_all(self) -> int:
        return self.__cursor.execute(f'SELECT COUNT(*) FROM {TABLE_NAME};').fetchone()[0]

    def __del__(self):
        self.__connect.close()
