from aiogram import types
from aiogram.filters import Command

#/start
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Я - бот приложения для тестирования. С помощью меня ты можешь ..."
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
<i>/start</i> - Начать работу с ботом
<i>/help</i> - Получить список команд
"""
    await message.answer(help_text, parse_mode="HTML")