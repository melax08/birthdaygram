import logging
import datetime as dt

from telegram.ext import ContextTypes, JobQueue

from bot.database import CheckTable, get_tables
from bot.exceptions import EmptyQuery
from bot.handlers.services import next_week_birthdays, today_birthdays
from bot.utils import send_message
from bot.constants.constants import RUN_SCHEDULER_HOURS

SCHEDULER_NAME = 'Birthdays check at {}'


async def tables_processing(tables: list) -> None:
    """Checks every table for today birthdays,
    sends a message to the user if any."""
    for chat_id in tables:
        try:
            today_message = today_birthdays(chat_id)
            logging.info(f'User: {chat_id} has today birthdays. '
                         f'Sending a message.')
            await send_message('\n'.join(today_message), chat_id)
        except EmptyQuery:
            pass

        try:
            week_message = next_week_birthdays(chat_id)
            logging.info(f'User: {chat_id} has next week birthdays. '
                         f'Sending a message.')
            await send_message('\n'.join(week_message), chat_id)
        except EmptyQuery:
            pass


def set_scheduler(job_queue: JobQueue) -> None:
    """Sets the job queue scheduler to run regularly."""
    if not RUN_SCHEDULER_HOURS:
        return
    times = [dt.time(hour=hour) for hour in RUN_SCHEDULER_HOURS]
    for time in times:
        job_queue.run_daily(
            callback=scheduler_callback,
            time=time,
            name=SCHEDULER_NAME.format(time.hour),
        )


async def scheduler_callback(context: ContextTypes) -> None:
    """Gets the list of user tables and check every table for today
    and next week birthdays."""
    logging.info('Started birthday reminder scheduler')
    tables = get_tables()
    await tables_processing(tables)
    logging.info('Finished birthday reminder scheduler')
