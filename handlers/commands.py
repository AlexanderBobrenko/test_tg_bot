from aiogram import types
from aiogram.filters import Command
from .keyboards import get_main_keyboard
from ..mocks.auth_mock import check_token, logout, authorize_user
from ..services.redis_service import set_user_status, get_user_status, set_user_token, delete_user_session, get_user_token
import uuid

#/start
async def start_command(message: types.Message):
    chat_id = message.chat.id
    status = get_user_status(chat_id)
    print(f"/start called with status: {status}")  # Отладочный вывод
    if not status:
        set_user_status(chat_id, 'Неизвестный')
    await message.answer(
        "Привет! Я - бот приложения для тестирования. С помощью меня ты можешь ...",
        reply_markup=get_main_keyboard()
    )

#/login
async def login_command(message: types.Message):
    chat_id = message.chat.id
    status = get_user_status(chat_id)
    print(f"/login called with status: {status}")  # Отладочный вывод
    if status == 'Неизвестный':
        set_user_status(chat_id, 'Анонимный')
        login_token = str(uuid.uuid4())
        set_user_token(chat_id, login_token)
        response = authorize_user(login_token)
        if response["status"] == "success":
            set_user_status(chat_id, "Авторизованный")
            await message.answer("Вы успешно авторизовались!")
        else:
            await message.answer("Ошибка авторизации.")
    elif status == 'Анонимный':
        await message.answer("Вы уже начали процесс авторизации.")
    elif status == 'Авторизованный':
        await message.answer("Вы уже авторизованы.")

#/logout
async def logout_command(message: types.Message):
    chat_id = message.chat.id
    refresh_token = get_user_token(chat_id)
    if refresh_token:
        response = logout(refresh_token)
        if response["status"] == "success":
            delete_user_session(chat_id)
            await message.answer("Вы успешно вышли из системы.")
    else:
        await message.answer("Вы не авторизованы.")

#/help
async def help_command(message: types.Message):
    help_text = """
<b><i>Доступные команды:</i></b>\n
<i>/start</i> - Начать работу с ботом
<i>/login</i> - Авторизоваться в боте
<i>/logout</i> - Выйти из системы\n
===========================\n
<i>/help</i> - Получить список команд
"""
    await message.answer(help_text, parse_mode="HTML")

#button "Авторизация"
async def auth_button(message: types.Message):
    chat_id = message.chat.id
    status = get_user_status(chat_id)
    if status == 'Неизвестный':
        await login_command(message)
    elif status == 'Анонимный':
        await message.answer("Вы уже начали процесс авторизации.")
    elif status == 'Авторизованный':
        await message.answer("Вы уже авторизованы.")

#button "Тесты"
async def tests_button(message: types.Message):
    chat_id = message.chat.id
    status = get_user_status(chat_id)
    if status == 'Авторизованный':
        await message.answer("Функция тестов пока не реализована.")
    else:
        await message.answer("Для доступа к тестам необходимо авторизоваться.")
#button "Помощь"
async def help_button_command(message: types.Message):
    await help_command(message)