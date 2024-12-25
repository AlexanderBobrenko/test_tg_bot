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