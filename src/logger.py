import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(message)s"
LOG_DT_FORMAT = "%d.%m.%Y %H:%M:%S"
LOG_BACKUP_COUNT = 5
LOG_MAX_SIZE = 50000000


def configure_logging(log_file_name: str) -> None:
    """Configure global logging."""
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / log_file_name
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=LOG_MAX_SIZE, backupCount=LOG_BACKUP_COUNT
    )
    logging.basicConfig(
        datefmt=LOG_DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler()),
    )

    # Disable information logs from telegram API itself requests.
    logging.getLogger("httpx").setLevel(logging.WARNING)
