import os
from datetime import datetime
import json
import asyncio
import logging
from aiogram import Dispatcher, types
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from handlers.common import variants_actions
from database import memory_bot
from other import my_func


class FSMObservation(StatesGroup):
    enter_family = State()
    enter_family_select_num = State()
    enter_query_client = State()
    enter_point_up = State()


async def enter_family(message: types.Message, state: FSMContext):
    user_data = await my_func.data_users_from_1c(message.text)
    if len(user_data) >= 1:
        text = "0: Нужного сотрудника нет в списке\n"
        for num, elem in enumerate(user_data):
            text += f"{num + 1}:{elem[0]}\n"
        await message.answer(f"{text}", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f"Под каким номером нужный сотрудник?")
        async with state.proxy() as data:
            data["Current proc"]["temp"] = user_data
        await FSMObservation.enter_family_select_num.set()
        await memory_bot.save_memory(state)
    else:
        await message.answer(f"Что-то таких в списках нет, попробуйте написать еще раз или проверьте данные в 1с",
                             reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Напишите ФАМИЛИЮ наблюдаемого:", reply_markup=types.ReplyKeyboardRemove())


async def enter_family_select_num(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            if 1 <= int(message.text) <= len(data.get("Current proc").get("temp")):
                await message.answer(f'{data["Current proc"]["temp"][int(message.text) - 1][0]} добавлен',
                                     reply_markup=types.ReplyKeyboardRemove())
                data["Current proc"]["Users"]= {
                    "User": data["Current proc"]["temp"][int(message.text) - 1][0],
                    'User_otdel': data["Current proc"]["temp"][int(message.text) - 1][1],
                    'User_filial': data["Current proc"]["temp"][int(message.text) - 1][2]
                }
                data["Current proc"].pop("temp")
                await message.answer("Напишите запрос клиента:", reply_markup=ReplyKeyboardRemove())
                await FSMObservation.enter_query_client.set()
            elif int(message.text) == 0:
                await message.answer(f"Проверьте правильность написания ФАМИЛИИ\nСкорей всего или допущена ошибка,"
                                     f"или сотрудника еще не успели создать в 1С"
                                     , reply_markup=types.ReplyKeyboardRemove())
                await message.answer("Напишите ФАМИЛИЮ наблюдаемого:", reply_markup=types.ReplyKeyboardRemove())
                data["Current proc"].pop("temp")
                await FSMObservation.enter_family.set()
            else:
                await message.reply(f'Издеваетесь?) Выберите значение от 0 до '
                                    f'{len(data.get("Current proc").get("temp"))}',
                                    reply_markup=types.ReplyKeyboardRemove())
                return
        await memory_bot.save_memory(state)
    else:
        await message.answer(f"Извините, давайте только по делу, укажите цифры с вашем ФИО:",
                             reply_markup=types.ReplyKeyboardRemove())


async def enter_query_client(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data.get("Current proc").get("query client") is None:
            data["Current proc"]["query client"] = message.text
        else:
            try:
                await message.delete()
            except MessageToDeleteNotFound:
                pass
            for msg_id in data["Current proc"]["message id to delete"]:
                try:
                    await message.bot.delete_message(message.from_user.id, msg_id)
                except MessageToDeleteNotFound:
                    continue
            data["Current proc"]["message id to delete"] = []
        for key1, value1 in data["Current proc"]["Check list"].items():
            temp_dict = dict()
            for key2, value2 in value1.items():
                if isinstance(value2, list):
                    temp_dict[key2] = value2
            if len(temp_dict) != 0:
                msg = await message.answer("Блок: {}\nВыставьте оценки".format(key1),
                                           reply_markup=ReplyKeyboardRemove())
                data["Current proc"]["message id to delete"].append(msg.message_id)
                for key2, value2 in temp_dict.items():
                    kb = InlineKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
                    for grade in value2:
                        kb.insert(InlineKeyboardButton(text=str(grade), callback_data="{}_{}".format(
                            key2.split(";")[0], str(grade))))
                    msg = await message.answer(key2.split(";")[1], reply_markup=kb)
                    data["Current proc"]["message id to delete"].append(msg.message_id)
                break
        else:
            await FSMObservation.enter_point_up.set()
            await message.answer("Напишите комментарий о возможных точках роста:")

    await memory_bot.save_memory(state)


async def enter_point_up(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["Current proc"]["point up"] = message.text
        data["Current proc"]["Time finish"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        data["Current proc"]["Duration"] = (datetime.strptime(data["Current proc"]["Time finish"], "%d.%m.%Y %H:%M:%S")
                                            - datetime.strptime(data["Current proc"]["Time start"], "%d.%m.%Y %H:%M:%S")
                                            ).total_seconds()
    await memory_bot.save_memory(state)
    await save_current_lesson(message, state)


async def save_current_lesson(message: types.Message, state: FSMContext):
    await message.answer("Сохраняю данные об обучении...", reply_markup=ReplyKeyboardRemove())
    async with state.proxy() as data:
        if await save_learn_to_file(data.as_dict()):
            await message.answer("Данные успешно сохранены!", reply_markup=ReplyKeyboardRemove())
            await variants_actions(message=message, state=state)
        else:
            await message.answer("Не могу сохранить данные в папку, попробуй повторить позднее",
                                 reply_markup=ReplyKeyboardRemove())


async def save_learn_to_file(my_data: dict) -> bool:
    for _ in range(20):
        try:
            path_to_total_file = os.sep * 2 + os.path.join("tg-storage01", "Аналитический отдел", "Проекты",
                                                           "Telegram Боты", "Бот по обучению V2", "Выгрузки",
                                                           "Наблюдение", "Данные об обучении {}.json".format(
                                                               datetime.now().replace(day=1).strftime("%d.%m.%Y")))
            if os.path.exists(path_to_total_file):
                with open(path_to_total_file, 'r', encoding="utf-8") as json_file:
                    data = json.load(json_file)
                data.append(my_data)
                with open(path_to_total_file, 'w', encoding="utf-8") as outfile:
                    json.dump(data, outfile, ensure_ascii=False)
            else:
                with open(path_to_total_file, 'w', encoding="utf-8") as outfile:
                    json.dump([my_data], outfile, ensure_ascii=False)
            return True
        except PermissionError:
            await asyncio.sleep(2)
            continue


async def query_check_list(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if query.message.message_id in data["Current proc"]["message id to delete"]:
            await query.message.delete()
            data["Current proc"]["message id to delete"].remove(query.message.message_id)
            temp_value = query.data.split("_")

            for key1_dict, value1_dict in data["Current proc"]["Check list"].items():
                for key2_dict in value1_dict.keys():
                    if temp_value[0] == key2_dict.split(";")[0]:
                        data["Current proc"]["Check list"][key1_dict][key2_dict] = temp_value[1]
                        break
    await memory_bot.save_memory(state)
    mark = False
    async with state.proxy() as data:
        if len(data["Current proc"]["message id to delete"]) == 1:
            await query.bot.delete_message(query.from_user.id, data["Current proc"]["message id to delete"][0])
            data["Current proc"]["message id to delete"].remove(data["Current proc"]["message id to delete"][0])
            mark = True
    if mark:
        await memory_bot.save_memory(state)
        await enter_query_client(query.message, state)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(enter_family, state=FSMObservation.enter_family)
    dp.register_message_handler(enter_family_select_num, state=FSMObservation.enter_family_select_num)
    dp.register_message_handler(enter_query_client, state=FSMObservation.enter_query_client)

    dp.register_callback_query_handler(query_check_list, state=FSMObservation.enter_query_client)
    dp.register_message_handler(enter_point_up,  state=FSMObservation.enter_point_up)