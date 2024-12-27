from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Авторизация")],
            [KeyboardButton(text="Тесты")],
            [KeyboardButton(text="Помощь")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return kb