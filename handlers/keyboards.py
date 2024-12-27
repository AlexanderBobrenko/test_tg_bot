from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.add(KeyboardButton('Авторизация'))
    kb.add(KeyboardButton('Тесты'))
    kb.add(KeyboardButton('Помощь'))
    return kb