from aiogram import types
from aiogram.filters import Command
from .keyboards import get_main_keyboard

#/start
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Я - бот приложения для тестирования. С помощью меня ты можешь ...",
        reply_markup=get_main_keyboard()
    )

#/login
async def login_command(message: types.Message):
    await message.answer(
        "Вам необходимо авторизоваться через GitHub, Яндекс ID или через код."
    )

#/help
async def help_command(message: types.Message):
    help_text = """
<b><i>Доступные команды:</i></b>
<br>
<i>/start</i> - Начать работу с ботом
<i>/login</i> - Авторизоваться в боте
<br>
===========================
<br>
<i>/help</i> - Получить список команд
"""
    await message.answer(help_text, parse_mode="HTML")

#button "Авторизация"
async def auth_button(message: types.Message):
    await message.answer("Функция авторизации пока не реализована.")

#button "Тесты"
async def tests_button(message: types.Message):
    await message.answer("Функция тестов пока не реализована.")

#button "Помощь"
async def help_button_command(message: types.Message):
    await help_command(message)