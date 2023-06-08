import os

from dotenv import load_dotenv

load_dotenv()

FULL_NAME_MAX_LEN = 50
SQLITE_DB_NAME = 'sqlite.db'
TOKEN = os.getenv('TOKEN')
TELEGRAM_ID = os.getenv('TELEGRAM_ID')
