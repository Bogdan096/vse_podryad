from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from datetime import datetime
import logging


# from database import memory_bot
# from other import my_func


class FSMCommon(StatesGroup):
    # auth = State()
    first_state = State()
    mob_state = State()
    adress_state = State()
    order_state = State()
    prom_state = State()


async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Приветствуем вас в нашем ресторане!\n")
    await FSMCommon.first_state.set()


async def cmd_infome(message: types.Message, state: FSMContext):
    aidi = message.from_user.id
    uname = message.from_user.username
    name = message.from_user.first_name
    surname = message.from_user.last_name
    async with state.proxy() as dats:
        dats["ID"] = message.from_user.id
        dats["Логин"] = message.from_user.username
        dats["Имя"] = message.from_user.first_name
        dats["Фамилия"] = message.from_user.last_name
    # await message.answer("Введите свое имя")


async def cmd_move(message: types.Message, state: FSMContext)
    pass


async def cmd_authorize(message: types.Message, state: FSMContext):
    await message.answer("Введите Имя")
    async with state.proxy() as datas:
        datas["Имя"] = message.text
        await FSMCommon.prom_state.set()
        await message.answer("Введите Фамилию")
        datas["Фамилия"] = message.text
        await FSMCommon.prom_state.set()
        await message.answer("Введите Отчество")
        datas["Отчество"] = message.text
        await FSMCommon.prom_state.set()
        await message.answer("Введите Номер Телефона")
    await FSMCommon.mob_state.set()


# async def name_input(message:types.Message, state: FSMContext):
#       async with state.proxy() as datas:
#          datas["Имя"] = message.text
#         await message.answer("Очень приятно! Введите адрес")
#         await FSMCommon.adress_state.set()

#  async def addres(message: types.Message,state: FSMContext):
#     async with state.proxy() as datas:
#         datas["Адрес"] = message.text
#     await message.answer("Введите номер телефона (8**********)")
#     await FSMCommon.mob_state.set()

async def mobile(message: types.Message, state: FSMContext):
    if not message.text.isnumeric() or len(message.text) != 11:
        await message.answer("Повторите ввод номера")
        return
    else:
        # async with state.proxy() as datas:
        #     datas["Номер"] = message.text
        await message.answer("Данные сохранены. Что будете заказывать?")
        await FSMCommon.order_state.set()


async def order(message: types.Message, state: FSMContext):
    if message.text.lower() == "конец":
        async with state.proxy() as datas:
            result = datas
        await message.answer("Имя клиента:{name}\n Адрес:{adress}\n Номер:{number}\n Заказ:{order}".format(
            name=result.get("Имя"),
            adress=result.get("Адрес"),
            number=result.get("Номер"),
            order=";".join(result.get("Заказ"))
        ))
        await state.finish()
    else:
        async with state.proxy() as datas:
            if datas.get("Заказ"):
                datas["Заказ"].append(message.text)
            else:
                datas["Заказ"] = [message.text]
        await message.answer("Еще один пункт добавлен. Напишите 'Конец'")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_move, commands="move")
    dp.register_message_handler(cmd_authorize, commands="authorization")
    dp.register_message_handler(cmd_authorize, state=FSMCommon.prom_state)
    # dp.register_message_handler(addres,state=FSMCommon.adress_state)
    dp.register_message_handler(mobile, state=FSMCommon.mob_state)
    dp.register_message_handler(order, state=FSMCommon.order_state)
