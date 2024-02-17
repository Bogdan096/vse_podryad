from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from datetime import datetime
import logging

from database import memory_bot
from other import my_func


class FSMCommon(StatesGroup):
    authorization = State()
    authorization_enter_family = State()
    authorization_select_num = State()
    choice = State()


async def cmd_start(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=True)
    async with state.proxy() as data:
        data["id_telegram"] = message.from_user.id
        kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        kb.insert(InlineKeyboardButton(text="Авторизоваться", callback_data="authorization"))
        await message.answer("Привет, {USERNAME}! Я буду помогать тебе с обучением.\n"
                             "Но, сначала мне нужно найти тебя в базе.\n"
                             "Нажми на кнопку ниже"
                             .format(USERNAME=message.from_user.first_name),
                             reply_markup=kb)
        await FSMCommon.authorization.set()

    await memory_bot.save_memory(state)


async def cmd_del_message(message: types.Message):
    await message.delete()


async def query_authorization(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer("Напишите вашу ФАМИЛИЮ:", reply_markup=ReplyKeyboardRemove())
    await query.answer()
    await FSMCommon.authorization_enter_family.set()
    await memory_bot.save_memory(state)


async def cmd_authorization(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=True)
    async with state.proxy() as data:
        data["id_telegram"] = message.from_user.id
    await message.answer("Напишите вашу ФАМИЛИЮ:", reply_markup=ReplyKeyboardRemove())
    await FSMCommon.authorization_enter_family.set()
    await memory_bot.save_memory(state)


async def authorization_enter_family(message: types.Message, state: FSMContext):
    user_data = await my_func.data_users_from_1c(message.text)
    if len(user_data) >= 1:
        text = "0: Меня нет в этом списке списке\n"
        for num, elem in enumerate(user_data):
            text += f"{num + 1}:{elem[0]}\n"
        await message.answer(f"{text}", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f"Вы под каким номером?")
        async with state.proxy() as data:
            data["User"] = user_data
        await FSMCommon.authorization_select_num.set()
        await memory_bot.save_memory(state)

    else:
        await message.answer(f"Что-то таких в списках нет, попробуйте написать еще раз или проверьте данные в 1с",
                             reply_markup=types.ReplyKeyboardRemove())


async def authorization_select_num(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            if 1 <= int(message.text) <= len(data["User"]):
                await message.answer(f"Отлично! {data['User'][int(message.text)-1][0]} так и запишем...")
                data["User_filial"] = data['User'][int(message.text)-1][2]
                data['User_otdel'] = data['User'][int(message.text)-1][1]
                data['User'] = data['User'][int(message.text) - 1][0]
            elif int(message.text) == 0:
                await message.answer("Вы точно написали вашу фамилию так-же как в 1С?\n"
                                     "Попробуйте написать еще раз.\nЕсли все равно не находит совпадения,"
                                     "то возможно вашу карточку еще не завели в сотрудниках 1С или допущена ошибка"
                                     , reply_markup=types.ReplyKeyboardRemove())
            else:
                await message.reply(f"Издеваетесь?) Выберите значение от 0 до {len(data['User'])}",
                                    reply_markup=types.ReplyKeyboardRemove())
                return

        await FSMCommon.choice.set()
        await memory_bot.save_memory(state)
        await variants_actions(message=message, state=state)
    else:
        await message.answer(f"Извините, давайте только по делу, укажите цифры с вашем ФИО:",
                             reply_markup=types.ReplyKeyboardRemove())


async def about_me(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        await message.answer("ID телеграмм: {}\n"
                             "ФИО: {}\n"
                             "Отдел: {}\n"
                             "Подразделение: {}".format(data.get("id_telegram"),
                                                        data.get("User"),
                                                        data.get("User_otdel"),
                                                        data.get("User_filial")),
                             reply_markup=types.ReplyKeyboardRemove())
        data["id_telegram"] = message.from_user.id


async def variants_actions(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not isinstance(data.get("User"), str):
            await message.delete()
            return
        data.pop("Current proc")
    kb = InlineKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    kb.insert(InlineKeyboardButton(text="Начать обучение", callback_data="start_teach"))
    kb.insert(InlineKeyboardButton(text="Начать наблюдение", callback_data="start_watch"))
    await message.answer("Что хочешь сделать?"
                         .format(USERNAME=message.from_user.first_name),
                         reply_markup=kb)
    await FSMCommon.choice.set()
    await memory_bot.save_memory(state)


async def query_variants_actions(query: types.CallbackQuery, state: FSMContext):
    if query.data == "start_teach":
        await query.message.answer("Напишите ФАМИЛИЮ обучаемого:", reply_markup=types.ReplyKeyboardRemove())
        async with state.proxy() as data:
            data["Current proc"] = {"Type": "Обучение", "Users": dict()}
        await state.set_state("FSMStudies:enter_family")
    elif query.data == "start_watch":
        await query.message.answer("Напишите ФАМИЛИЮ наблюдаемого:", reply_markup=types.ReplyKeyboardRemove())
        async with state.proxy() as data:
            data["Current proc"] = {"Type": "Наблюдение",
                                    "Users": dict(),
                                    "Time start": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                                    "Time finish": None,
                                    "Duration": None,
                                    "message id to delete": [],
                                    "Check list": {
                                        "Установление контакта": {
                                            "1;Проявил инициативу и сам подошел к клиенту": [0, 2],
                                            "2;Поприветствовал покупателя, представился": [0, 1, 2],
                                            "3;Применил фразу на установление контакта"
                                            " Клиент охотно вступил в диалог": [0, 2],
                                            "4;Узнал имя покупателя": [0, 2],
                                        },
                                        "Выяснение потребностей": {
                                            "5;Уточнил запрос клиента, используя воронку вопросов. "
                                            "опросы построены грамотно и последовательно": [0, 1, 3],
                                            "6;Резюмировал выявленные потребности": [0, 3],
                                        },
                                        "Презентация": {
                                            "7;Сотрудник хорошо ориентируется в ассортименте": [0, 3],
                                            "8;Говорит простым языком, объясняет терминологию": [0, 1],
                                            "9;В предложении товара были использованы выявленные точки воздействия":
                                                [0, 1, 3],
                                            "10;Сделал комплексное предложение (как минимум, два "
                                            "дополнительных товара, которые могут подойти)": [0, 2],
                                        },
                                        "Работа с возражениями": {
                                            "11;Работал с возражением по алгоритму": [0, 2],
                                            "12;Говорил убедительно и грамотно, опираясь на потребности клиента":
                                                [0, 1, 2],
                                        },
                                        "Завершение диалога": {
                                            "13;Предложил дополнительные услуги "
                                            "(нарезка, монтаж, доставка, подъем на этаж)": [0, 2],
                                            "14;Договорился с клиентом о дальнейших действиях. Пригласил приехать в"
                                            " магазин или договарился о следующем звонке": [0, 2],
                                            "15;Вежливо завершает разговор": [0, 1],
                                        },
                                        "Общее впечатление ": {
                                            "16;Доброжелательное выражение лица и интонация на "
                                            "протяжении всего диалога": [0, 2],
                                            "17;Нет долгих пауз и неуместных повторений вопросов ": [0, 2],
                                            "18;Производит впечатление профессионала, убедителен в коммуникации": [0, 3],
                                        }
                                    }}
        await state.set_state("FSMObservation:enter_family")
    else:
        return
    await query.message.delete()
    await memory_bot.save_memory(state)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_authorization, commands="authorization", state="*")
    dp.register_message_handler(about_me, commands="about_me", state="*")
    dp.register_message_handler(variants_actions, commands="actions", state="*")
    dp.register_callback_query_handler(query_variants_actions, state=FSMCommon.choice)

    dp.register_message_handler(cmd_del_message, state=[FSMCommon.authorization, FSMCommon.choice,
                                                        "FSMStudies:add_user_or_next_step",
                                                        "FSMStudies:choice_train",
                                                        "FSMStudies:resume",
                                                        "FSMStudies:time"])
    dp.register_callback_query_handler(query_authorization, state=FSMCommon.authorization)
    dp.register_message_handler(authorization_enter_family, state=FSMCommon.authorization_enter_family)
    dp.register_message_handler(authorization_select_num, state=FSMCommon.authorization_select_num)
