import asyncio
import datetime as dt
import logging

from telegram.ext import ContextTypes, JobQueue

from bot.constants.constants import RUN_SCHEDULER_HOURS
from bot.constants.logging_messages import (
    SCHEDULER_FINISH_LOG,
    SCHEDULER_NEXT_WEEK_BIRTHDAYS_LOG,
    SCHEDULER_START_LOG,
    SCHEDULER_TODAY_BIRTHDAYS_LOG,
)
from bot.database import UserTable
from bot.exceptions import EmptyQuery
from bot.handlers.services import next_week_birthdays, today_birthdays
from bot.utils import send_message

SCHEDULER_NAME = "Birthdays check at {}"


async def _check_birthdays_task(chat_id):
    """Checks today and next week birthdays for current the telegram
    chat id."""
    try:
        today_message = await today_birthdays(chat_id)
        logging.info(SCHEDULER_TODAY_BIRTHDAYS_LOG.format(chat_id))
        await send_message("\n".join(today_message), chat_id)
    except EmptyQuery:
        pass

    try:
        week_message = await next_week_birthdays(chat_id)
        logging.info(SCHEDULER_NEXT_WEEK_BIRTHDAYS_LOG.format(chat_id))
        await send_message("\n".join(week_message), chat_id)
    except EmptyQuery:
        pass


async def tables_processing(tables: list) -> None:
    """Main coroutine. Creates tasks to check all tables in database for
    today and next week birthdays."""
    tasks = [
        asyncio.ensure_future(_check_birthdays_task(chat_id)) for chat_id in tables
    ]
    await asyncio.wait(tasks)


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
    logging.info(SCHEDULER_START_LOG)
    tables = await UserTable.get_table_names()
    await tables_processing(tables)
    logging.info(SCHEDULER_FINISH_LOG)
