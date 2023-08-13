import os

from dotenv import load_dotenv

load_dotenv()

FULL_NAME_MAX_LEN = 50
BIRTHDAYGRAM_LOG_NAME = 'birthdaygram.log'

DATE_FORMAT = '%d.%m.%Y'

TOKEN = os.getenv('TOKEN')
db_user = os.getenv("POSTGRES_USER", default='birthdaygram')
db_password = os.getenv("POSTGRES_PASSWORD", default='123456')
db_host = os.getenv("DB_HOST", default='db')
db_port = os.getenv("DB_PORT", default='5432')
db_name = os.getenv("DB_NAME", default='birthdaygram')
SQL_SETTINGS = (
    f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
)
ECHO = int(os.getenv('ECHO', default=0))
