from telegram import ReplyKeyboardMarkup

MAIN_BUTTONS = ReplyKeyboardMarkup([
        ['/add', '/show_all']
    ], resize_keyboard=True, input_field_placeholder='Выберите действие:')
YES_NO_BUTTONS = ReplyKeyboardMarkup([['Да', 'Нет']], input_field_placeholder='Все корректно?')
