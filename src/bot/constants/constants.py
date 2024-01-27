import os

from dotenv import load_dotenv

load_dotenv()

FULL_NAME_MAX_LEN: int = 50
BIRTHDAYGRAM_LOG_NAME: str = "birthdaygram.log"

DATE_FORMAT: str = "%d.%m.%Y"

BOT_TIMEZONE: str = os.getenv("TZ", default="Europe/Moscow")

RUN_SCHEDULER_HOURS: tuple = tuple(
    map(int, (os.getenv("RUN_SCHEDULER_HOURS", default="12 6").split()))
)

TOKEN: str = os.getenv("TOKEN")
db_user: str = os.getenv("POSTGRES_USER", default="birthdaygram")
db_password: str = os.getenv("POSTGRES_PASSWORD", default="123456")
db_host: str = os.getenv("DB_HOST", default="db")
db_port: str = os.getenv("DB_PORT", default="5432")
db_name: str = os.getenv("DB_NAME", default="birthdaygram")
SQL_SETTINGS: str = (
    f"postgresql+asyncpg:" f"//{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
ECHO: int = int(os.getenv("ECHO", default=0))
