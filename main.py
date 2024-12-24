import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from config import TOKEN
from handlers.commands import start_command, login_command
from handlers.messages import start_test_message

# Создаем экземпляр бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Регистрация команд
dp.message.register(start_command, Command(commands=['start']))
dp.message.register(login_command, Command(commands=['login']))

# Регистрация текстовых сообщений
dp.message.register(start_test_message, Text(text='Начать тест'))


# Основная функция для запуска бота
async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Ошибка: {e}")


# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
