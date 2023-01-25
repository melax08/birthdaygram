import sqlite3

DATABASE_NAME = 'birthdays.db'


class Database:
    def __init__(self):
        self.__connect = sqlite3.connect(DATABASE_NAME)
        self.__cursor = self.__connect.cursor()

    def create_table(self) -> None:
        try:
            self.__cursor.execute("""CREATE TABLE birthdays(full_name VARCHAR(255), birth_date DATE)""")
            print('Database was succesfuly created!')
        except sqlite3.OperationalError as error:
            print(f'Error! {error}')

    def new_record(self, name: str, birthday: str):
        self.__cursor.execute(f"INSERT INTO birthdays (full_name, birth_date) VALUES ('{name}', '{birthday}');")
        self.__connect.commit()

    def today_birthdays(self) -> list:
        return self.__cursor.execute(f"SELECT * FROM birthdays WHERE strftime('%m-%d', birth_date) = strftime('%m-%d',date('now', 'localtime'));").fetchall()

    def __del__(self):
        self.__connect.close()
