from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from datetime import datetime
import logging

# from database import memory_bot
# from other import my_func


class FSMCommon(StatesGroup):

    order_state = State()
    prom_state = State()
    check_state = State()
    my_order_state = State()
    name_state = State()
    surname_state = State()
    fathername_state = State()
    numb_state = State()
    choice_select_move = State()




async def cmd_infome(message: types.Message, state: FSMContext):
    if await state.get_data("Номер"):
        async with state.proxy() as datas:
            await message.answer("Ваше имя: {name}\n"
                                 "Ваша фамилия: {surname}\n"
                                 "Ваше отчество: {fathername}\n"
                                 "Ваш номер: {number}\n"
                                 "Ваш ID: {id}\n"
                                 "Ваше имя TG: {ntg}\n"
                                 "Ваша фамилия TG: {stg}\n"
                                 "Ваш логин: {login}".format(name=datas.get("name"),
                                                             surname=datas.get("Фамилия"),
                                                             fathername=datas.get("Отчество"),
                                                             number=datas.get("Номер"),
                                                             id=datas.get("ID TG"),
                                                             ntg=datas.get("Имя TG"),
                                                             stg=datas.get("Фамилия TG"),
                                                             login=datas.get("Логин TG")))

    else:
        await message.answer("Вы неавторизованы. Авторизуйтесь.")
        await authorization(message, state)





async def cmd_move(message: types.Message, state: FSMContext):

    kb = ReplyKeyboardMarkup(row_width=3)
    kb.row(KeyboardButton(text=1), KeyboardButton(text=2), KeyboardButton(text=2), KeyboardButton(text=2))
    kb.insert(KeyboardButton(text=2))
    kb.insert(KeyboardButton(text="a"))
    kb.insert(KeyboardButton(text="b"))
    kb.insert(KeyboardButton(text="c"))



    if message.text == "/move":
        await message.answer("Выберите номер действия:\n"
                             "1 - Сделать заказ\n"
                             "2 - Мои заказы", reply_markup=kb)

        await FSMCommon.choice_select_move.set()
    elif int(message.text) == 1:
        if await state.get_data("Номер"):
            await message.answer("Что будете заказывать?")
            await FSMCommon.order_state.set()
        else:
            await message.answer("Вы не можете сделать заказ, авторизуйтесь для начала работы.")
            await authorization(message, state)
    elif int(message.text) == 2:
        if await state.get_data("Номер"):
            # await message.answer("Тут ваши заказы")

            await message.answer("Вот ваш заказ")
            print("We in Func")
            async with state.proxy() as datas:
                if datas.get("Заказы"):
                    for index, elem in enumerate(datas.get("Заказы")):
                        await message.answer(
                            f"Ваши заказы: {index + 1}-й заказ - {len(elem)} {elem}")

                else:
                    await message.answer("Заказов больше нет")

        else:
            await message.answer("Вы не можете посмотреть заказы, авторизуйтесь.")
            await authorization(message, state)

    else:
        await message.answer("Что то пошло не так. Повторите ввод")
        return

async def order(message: types.Message, state: FSMContext):
    async with state.proxy() as datas:
        if not datas.get("Заказы"):
            datas["Заказы"] = []
        if not datas.get("Текущий заказ"):
            datas["Текущий заказ"] = []
        if message.text.lower() != "конец":
            datas["Текущий заказ"].append(message.text)
            await message.answer("Еще один пункт добавлен. Напишите 'Конец', если хотите завершить заказ")
        else:
            datas["Заказы"].append((datas["Текущий заказ"].copy()))
            datas.pop("Текущий заказ")
            await message.answer("Заказ сформирован.")
            await message.answer("Выберите номер действия:\n"
                                 "1 - Сделать заказ\n"
                                 "2 - Мои заказы")
            await FSMCommon.choice_select_move.set()

# async def my_order(message: types.Message, state: FSMContext):
#     ord_count = 1
#     await message.answer("Вот ваш заказ")
#     print("We in Func")
#     async with state.proxy() as datas:
#         while datas[f"{ord_count}-й заказ"] != "":
#             await message.answer(f"Ваши заказы: {ord_count}-й заказ - {datas[f'Количество позиций заказа {ord_count}']}")
#             ord_count += 1
#         else:
#             await message.answer("Заказов больше нет")

async def cmd_start(message: types.Message, state: FSMContext):
    """При старте, начинаем процедуру авторизации"""
    await authorization(message, state)

async def authorization(message: types.Message, state: FSMContext):
    """Запрашиваем имя, сбрасываем память, переводим дальше"""
    await message.answer("Введите имя: ")
    await state.reset_state()
    await FSMCommon.name_state.set()

async def surname(message: types.Message, state: FSMContext):
    """Запрашиваем фамилию, сохраняем имя, переводим дальше"""
    async with state.proxy() as datas:
        datas["name"] = message.text
        datas["ID TG"] = message.from_user.id
        datas["Логин TG"] = message.from_user.username
        datas["Имя TG"] = message.from_user.first_name
        datas["Фамилия TG"] = message.from_user.last_name

    await message.answer("Введите фамилию")
    await FSMCommon.surname_state.set()

async def fathername(message: types.Message, state: FSMContext):
    """Запрашиваем отчество, сохраняем фамилию, переводим дальше"""
    async with state.proxy() as datas:
        datas["Фамилия"] = message.text
    await message.answer("Введите отчество:")
    await FSMCommon.fathername_state.set()

async def waiting_fname(message: types.Message, state: FSMContext):
    """Запрашиваем номер, сохраняем отчество, переводим дальше"""
    async with state.proxy() as datas:
        datas["Отчество"] = message.text
    await message.answer("Введите номер телефона")
    await FSMCommon.numb_state.set()

async def check_number(message: types.Message, state: FSMContext):
    """Проверяем номер, сохраняем номер, завершаем авторизацию"""
    if not message.text.isnumeric() or len(message.text) != 11:
        await message.answer("Повторите ввод номера")
        return
    else:
        async with state.proxy() as datas:
            datas["Номер"] = message.text
        await message.answer("Авторизация завершена. Нажмите /move, для начала заказа")
        await FSMCommon.prom_state.set()



def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands = "start", state="*")
    dp.register_message_handler(cmd_infome, commands = "info_about_me", state="*")
    dp.register_message_handler(cmd_move, commands="move", state="*")
    dp.register_message_handler(cmd_move, state=FSMCommon.choice_select_move)
    dp.register_message_handler(surname, state = FSMCommon.name_state)
    dp.register_message_handler(fathername, state=FSMCommon.surname_state)
    dp.register_message_handler(waiting_fname, state=FSMCommon.fathername_state)
    dp.register_message_handler(check_number, state=FSMCommon.numb_state)
    dp.register_message_handler(order,state=FSMCommon.order_state)
    # dp.register_message_handler(my_order, state=FSMCommon.my_order_state)

