from aiogram.utils import executor
from aiogram.types import BotCommand
import logging

from create_bot import dp
from handlers import common, studies

from database import memory_bot

logging.basicConfig(level=logging.INFO)


async def on_startup(_):

    logging.info("Бот по обучению онлайн")
    # await memory_bot.load_memory(dp)
    commands = [
        BotCommand(command="/start", description="Начало работы"),
        BotCommand(command="/move", description="Доступные действия"),
        BotCommand(command="/info_about_me", description="Информация о пользователе"),

    ]
    await dp.bot.set_my_commands(commands)

common.register_handlers(dp)
studies.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
