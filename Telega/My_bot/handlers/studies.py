
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from handlers.common import FSMCommon
from other import my_func


class FSMStudies(StatesGroup):
    enter_family = State()
    enter_family_select_num = State()



async def enter_family(message: types.Message, state: FSMContext):

    await state.set_state("1")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(enter_family, state=FSMStudies.enter_family)
    dp.register_message_handler(enter_family, state="1")
    # dp.register_message_handler(enter_family_select_num, state=FSMStudies.enter_family_select_num)


