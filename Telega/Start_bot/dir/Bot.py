import asyncio
import logging
from aiogram import Router
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart
from Telega.start_bot.dir import main_body

logging.basicConfig(level=logging.INFO)

bot = Bot(token="7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
router = Router()
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message:types.Message):
    await message.answer("👋 Добро пожаловать! Для начала тебе необходимо авторизоваться. Нажми на команду 👇 (/authorization)")



async def main():
    dp.include_router(main_body.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())