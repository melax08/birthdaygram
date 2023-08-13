from telegram import ReplyKeyboardMarkup

ADD_BUTTON = '✅ Добавить'
DELETE_BUTTON = '❌ Удалить'
ALL_BUTTON = '🗂 Список'
TODAY_BUTTON = 'Сегодня'
WEEK_BUTTON = 'Неделя'
MONTH_BUTTON = 'Месяц'
HELP_BUTTON = '❓ Помощь'

MAIN_BUTTONS = ReplyKeyboardMarkup(
    [[ADD_BUTTON, DELETE_BUTTON, ALL_BUTTON],
     [TODAY_BUTTON, WEEK_BUTTON, MONTH_BUTTON],
     [HELP_BUTTON]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие:'
)

YES_NO_BUTTONS = ReplyKeyboardMarkup(
    [['Да', 'Нет']],
    resize_keyboard=True,
    input_field_placeholder='Все корректно?'
)
