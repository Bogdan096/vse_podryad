import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandStart

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6579477792:AAFzRL7T-noWx3Ce74mR7qgfE-xCBuzaQYM")
dp = Dispatcher()

# @dp.message(CommandStart())
# async def cmd_start(message:types.Message):
#     await message.answer('Все работает')

# @dp.message(CommandStart())
# async def cmd_start(message:types.Message):
#     await message.answer("Проверка запущена")

async def main():
    await dp.start_polling((bot))

if __name__ == "__main__":
    asyncio.run(main())