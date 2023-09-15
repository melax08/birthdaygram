USER_ADD_LOG = 'User {} added a new person to his birthdate list: {} {}'

SEND_ALL_RECORDS_LOG = 'Sent message with all records to user {}. Message: {}'

SEND_TODAY_BIRTHDAYS_LOG = (
    'Sent message about today birthdays to user {}. Message: {}'
)

SEND_NEXT_INTERVAL_BIRTHDAYS_LOG = (
    'Sent message about next {} days birthdays to user {}. Message: {}'
)

USER_DELETE_LOG = 'The user {} removed a person {} from his list of birthdays.'

START_BOT_LOG = 'Someone starts the bot: {}'

EXCEPTION_LOG = 'Exception while handling an update:'

# Scheduler log messages
SCHEDULER_START_LOG = 'Started birthday reminder scheduler'
SCHEDULER_FINISH_LOG = 'Finished birthday reminder scheduler'
SCHEDULER_TODAY_BIRTHDAYS_LOG = (
    'User: {} has today birthdays. Sending a message.'
)
SCHEDULER_NEXT_WEEK_BIRTHDAYS_LOG = (
    'User: {} has next week birthdays. Sending a message.'
)
