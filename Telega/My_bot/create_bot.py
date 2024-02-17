from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage
bot = Bot(token="6579477792:AAFzRL7T-noWx3Ce74mR7qgfE-xCBuzaQYM")
dp = Dispatcher(bot, storage=storage())
