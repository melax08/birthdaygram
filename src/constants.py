import os

from dotenv import load_dotenv

load_dotenv()

FULL_NAME_MAX_LEN = 50
SQLITE_DB_NAME = 'sqlite.db'
TOKEN = os.getenv('TOKEN')
TELEGRAM_ID = os.getenv('TELEGRAM_ID')
BIRTHDAYGRAM_LOG_NAME = 'birthdaygram.log'

if int(os.getenv('LOCAL', default=0)):
    sql_settings = f'sqlite:///{SQLITE_DB_NAME}'
    ECHO = True
else:
    db_user = os.getenv("POSTGRES_USER", default='birthdaygram')
    db_password = os.getenv("POSTGRES_PASSWORD", default='123456')
    db_host = os.getenv("DB_HOST", default='db')
    db_port = os.getenv("DB_PORT", default='5432')
    db_name = os.getenv("DB_NAME", default='birthdaygram')
    sql_settings = (
        f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    )
    ECHO = False
