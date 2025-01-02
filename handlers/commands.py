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
        "Добро пожаловать! Я — ваш помощник в приложении для тестирования. "
        "С моей помощью вы можете проходить тесты и отслеживать свои результаты.",
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
        print(f"Authorization response: {response}")  # Отладочный вывод
        if response["status"] == "success":
            set_user_status(chat_id, "Авторизованный")
            print(f"User {chat_id} status updated to: Авторизованный")  # Отладочный вывод
            await message.answer(
                "🎉 Вы успешно авторизовались! Теперь вам доступны все функции.",
                reply_markup=get_main_keyboard(is_authorized=True)
            )
        else:
            await message.answer("❌ Ошибка авторизации. Пожалуйста, попробуйте снова.")
    elif status == 'Анонимный':
        await message.answer("🔑 Вы уже начали процесс авторизации. Пожалуйста, завершите его.")
    elif status == 'Авторизованный':
        await message.answer("✅ Вы уже авторизованы. Нет необходимости входить снова.")

#/logout
async def logout_command(message: types.Message):
    chat_id = message.chat.id
    refresh_token = get_user_token(chat_id)
    print(f"/logout called with token: {refresh_token}")  # Отладочный вывод
    if refresh_token:
        response = logout(refresh_token)
        print(f"Logout response: {response}")  # Отладочный вывод
        if response["status"] == "success":
            delete_user_session(chat_id)
            print(f"User {chat_id} session deleted. New status: {get_user_status(chat_id)}")  # Отладочный вывод
            await message.answer(
                "👋 Вы успешно вышли из системы.",
                reply_markup=get_main_keyboard(is_authorized=False)
            )
    else:
        await message.answer("⚠️ Вы не авторизованы. Войдите в систему, чтобы продолжить.")

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
    print(f"auth_button called with status: {status}")  # Отладочный вывод
    if status == 'Неизвестный':
        await login_command(message)
    elif status == 'Анонимный':
        await message.answer("🔑 Вы уже начали процесс авторизации. Пожалуйста, завершите его.")
    elif status == 'Авторизованный':
        await message.answer("✅ Вы уже авторизованы. Нет необходимости входить снова.")

#button "Тесты"
async def tests_button(message: types.Message):
    chat_id = message.chat.id
    status = get_user_status(chat_id)
    print(f"tests_button called with status: {status}")  # Отладочный вывод
    if status == 'Авторизованный':
        await message.answer("📚 Функция тестов пока не реализована.")
    else:
        await message.answer("🔒 Для доступа к тестам необходимо авторизоваться. Используйте команду /login.")

#button "Помощь"
async def help_button_command(message: types.Message):
    await help_command(message)