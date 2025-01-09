from aiogram import types
from aiogram.filters import Command
from .keyboards import get_main_keyboard
from ..mocks.auth_mock import check_token, logout, authorize_user
from ..mocks.main_module_mock import get_tests, get_test_details, get_test_questions, create_attempt, submit_answer, get_attempt_results
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

#/show_tests
async def list_tests(message: types.Message):
    tests = get_tests()
    if not tests:
        await message.answer("Тесты не найдены.")
        return

    response = "📚 Доступные тесты:\n"
    for test in tests:
        response += f"{test['id']}. {test['name']} — {test['description']}\n"

    await message.answer(response)

#/test_details
async def test_details_command(message: types.Message):
    text = message.text.split()
    print(f"/test_details called with args: {text}")  # Отладочный вывод
    if len(text) < 2:
        await message.answer("Пожалуйста, укажите ID теста.")
        return
    
    test_id = int(text[1])
    test = get_test_details(test_id)
    print(f"Test details: {test}")  # Отладочный вывод
    
    if test:
        response = f"Название: {test['name']}\nОписание: {test['description']}"
    else:
        response = "Тест не найден."
    
    await message.answer(response)

#/create_attempt
async def create_attempt_command(message: types.Message):
    text = message.text.split()
    print(f"/create_attempt called with args: {text}")  # Отладочный вывод
    if len(text) < 2:
        await message.answer("Пожалуйста, укажите ID теста.")
        return
    
    test_id = int(text[1])
    user_id = message.from_user.id
    attempt = create_attempt(test_id, user_id)
    print(f"Attempt: {attempt}")  # Отладочный вывод
    
    if attempt:
        response = f"Попытка теста '{test_id}' создана. ID попытки: {attempt['id']}."
    else:
        response = "Ошибка создания попытки."
    
    await message.answer(response)

#/submit_answer
async def submit_answer_command(message: types.Message):
    text = message.text.split()
    if len(text) != 4:
        await message.answer("Используйте: /submit_answer <ID попытки> <ID вопроса> <номер ответа>")
        return
    
    attempt_id, question_id, answer = map(int, text[1:])
    result = submit_answer(attempt_id, question_id, answer)
    
    if result["status"] == "success":
        response = "Ответ принят."
    else:
        response = result["message"]
    
    await message.answer(response)

#/get_results
async def get_results_command(message: types.Message):
    text = message.text.split()
    if len(text) < 2:
        await message.answer("Пожалуйста, укажите ID попытки.")
        return
    
    attempt_id = int(text[1])
    results = get_attempt_results(attempt_id)
    
    if results["status"] == "success":
        response = f"Результаты попытки {attempt_id}:\n"
        for result in results["results"]:
            response += (f"Вопрос: {result['question_text']}\n"
                         f"Ваш ответ: {result['user_answer']}\n"
                         f"Правильный ответ: {result['correct_answer']}\n"
                         f"Правильно: {'Да' if result['is_correct'] else 'Нет'}\n\n")
        response += (f"Всего правильных ответов: {results['total_correct']}\n"
                     f"Всего вопросов: {results['total_questions']}\n")
    else:
        response = results["message"]
    
    await message.answer(response)

#/help
async def help_command(message: types.Message):
    help_text = """
<b><i>Доступные команды:</i></b>\n
<i>/start</i> - Начать работу с ботом
<i>/login</i> - Авторизоваться в боте
<i>/logout</i> - Выйти из системы
<i>/show_tests</i> - Показать список тестов
<i>/test_details *id теста*</i> - Показать детали теста
<i>/create_attempt *id теста*</i> - Начать попытку теста
<i>/submit_answer *id попытки* *№ вопроса* *№ ответа*</i> - Ответить на вопрос
<i>/get_results *id попытки*</i> - Показать результаты теста
\n
================================================\n
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