import os
from datetime import datetime
import pandas as pd
import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from handlers.common import variants_actions
from database import memory_bot
from other import my_func


class FSMStudies(StatesGroup):
    enter_family = State()
    enter_family_select_num = State()
    add_user_or_next_step = State()
    choice_train = State()
    enter_subject = State()
    enter_target = State()
    resume = State()
    time = State()
    grade = State()
    comment = State()
    control = State()


async def enter_family(message: types.Message, state: FSMContext):
    kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    kb.insert(InlineKeyboardButton(text="Добавить еще одного сотрудника", callback_data="add"))
    kb.insert(InlineKeyboardButton(text="Перейти к выбору вида обучения", callback_data="next"))
    user_data = await my_func.data_users_from_1c(message.text)
    if len(user_data) >= 1:
        text = "0: Нужного сотрудника нет в списке\n"
        for num, elem in enumerate(user_data):
            text += f"{num + 1}:{elem[0]}\n"
        await message.answer(f"{text}", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f"Под каким номером нужный сотрудник?")
        async with state.proxy() as data:
            data["Current proc"]["temp"] = user_data
        await FSMStudies.enter_family_select_num.set()
        await memory_bot.save_memory(state)
    else:
        await message.answer(f"Что-то таких в списках нет, попробуйте написать еще раз или проверьте данные в 1с",
                             reply_markup=types.ReplyKeyboardRemove())
        async with state.proxy() as data:
            if len(data.get("Current proc").get("Users")) > 0:
                await message.answer("Выберите следующие действие:", reply_markup=kb)
                await FSMStudies.add_user_or_next_step.set()
            else:
                await message.answer("Напишите ФАМИЛИЮ обучаемого:", reply_markup=types.ReplyKeyboardRemove())


async def enter_family_select_num(message: types.Message, state: FSMContext):
    kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    kb.insert(InlineKeyboardButton(text="Добавить еще одного сотрудника", callback_data="add"))
    kb.insert(InlineKeyboardButton(text="Перейти к выбору вида обучения", callback_data="next"))
    if message.text.isdigit():
        async with state.proxy() as data:
            if 1 <= int(message.text) <= len(data.get("Current proc").get("temp")):
                await message.answer(f'{data["Current proc"]["temp"][int(message.text) - 1][0]} добавлен',
                                     reply_markup=types.ReplyKeyboardRemove())
                data["Current proc"]["Users"][data["Current proc"]["temp"][int(message.text) - 1][0]] = {
                    'User_otdel': data["Current proc"]["temp"][int(message.text) - 1][1],
                    'User_filial': data["Current proc"]["temp"][int(message.text) - 1][2]
                }
                data["Current proc"].pop("temp")
                await message.answer("Выберите следующие действие:", reply_markup=kb)
                await FSMStudies.add_user_or_next_step.set()

            elif int(message.text) == 0:
                await message.answer(f"Проверьте правильность написания ФАМИЛИИ\nСкорей всего или допущена ошибка,"
                                     f"или сотрудника еще не успели создать в 1С"
                                     , reply_markup=types.ReplyKeyboardRemove())
                if len(data.get("Current proc").get("Users")) > 0:
                    await message.answer("Выберите следующие действие:", reply_markup=kb)
                    await FSMStudies.add_user_or_next_step.set()
                else:
                    await message.answer("Напишите ФАМИЛИЮ обучаемого:", reply_markup=types.ReplyKeyboardRemove())
                    data["Current proc"].pop("temp")
                    await FSMStudies.enter_family.set()

            else:
                await message.reply(f'Издеваетесь?) Выберите значение от 0 до '
                                    f'{len(data.get("Current proc").get("temp"))}',
                                    reply_markup=types.ReplyKeyboardRemove())
                return
        await memory_bot.save_memory(state)

    else:
        await message.answer(f"Извините, давайте только по делу, укажите цифры с вашем ФИО:",
                             reply_markup=types.ReplyKeyboardRemove())


async def add_user_or_next_step(query: types.CallbackQuery, state: FSMContext):
    if query.data == "add":
        await query.message.answer("Напишите ФАМИЛИЮ обучаемого:", reply_markup=types.ReplyKeyboardRemove())
        await FSMStudies.enter_family.set()
        await query.message.delete()
    elif query.data == "next":
        await FSMStudies.choice_train.set()
        await query.message.delete()
        async with state.proxy() as data:
            data["Current proc"]["training"] = {
                "Деловая игра": False,
                "Опрос": False,
                "1с/ПК/ТСД": False,
                "Практика": False,
                "Теория": False,
                "Перейти к теме обучения": False
            }
            await query.message.answer("Отметьте нужные виды обучения:", reply_markup=await get_kb_choice_train(
                data["Current proc"]["training"]))
    else:
        return
    await memory_bot.save_memory(state)


async def get_kb_choice_train(my_dict: dict) -> InlineKeyboardMarkup():
    kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    for key, value in my_dict.items():
        if value:
            temp_value = "✅"
        else:
            if key != "Перейти к теме обучения":
                temp_value = "❌"
            else:
                temp_value = ""
        kb.insert(InlineKeyboardButton(text="{} {}".format(key, temp_value),
                                       callback_data="{};{}".format(key, value)))
    return kb


async def choice_train(query: types.CallbackQuery, state: FSMContext):
    list_data = query.data.split(";")
    if list_data[0] in ["Деловая игра", "Опрос", "1с/ПК/ТСД", "Практика", "Теория"]:
        async with state.proxy() as data:
            if list_data[1] == "True":
                data["Current proc"]["training"][list_data[0]] = False
            else:
                data["Current proc"]["training"][list_data[0]] = True
            await query.bot.edit_message_reply_markup(query.message.chat.id,
                                                      query.message.message_id,
                                                      reply_markup=await get_kb_choice_train(
                                                          data["Current proc"]["training"])
                                                      )
    elif list_data[0] == "Перейти к теме обучения":
        async with state.proxy() as data:
            if data["Current proc"]["training"]["Деловая игра"] or \
                data["Current proc"]["training"]["Опрос"] or \
                data["Current proc"]["training"]["1с/ПК/ТСД"] or \
                data["Current proc"]["training"]["Практика"] or \
                data["Current proc"]["training"]["Теория"]:
                await FSMStudies.enter_subject.set()
                await query.message.delete()
                await query.message.answer("Напишите тему обучения:", reply_markup=types.ReplyKeyboardRemove())
            else:
                await query.answer("Нужно выбрать хотя-бы один вид обучения!", show_alert=True)
    else:
        return
    await memory_bot.save_memory(state)


async def enter_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["Current proc"]["subject"] = message.text
    await FSMStudies.enter_target.set()
    await memory_bot.save_memory(state)
    await message.answer("Напишите цель обучения:", reply_markup=types.ReplyKeyboardRemove())


async def enter_target(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["Current proc"]["target"] = message.text
    await FSMStudies.resume.set()
    await memory_bot.save_memory(state)
    await show_resume(message=message, state=state)


async def show_resume(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        current_dict: dict = data.get("Current proc")
        if len(current_dict) == 5:
            kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            kb.insert(InlineKeyboardButton(text="Изменить данные", callback_data="BACK"))
            kb.insert(InlineKeyboardButton(text="Начать обучение", callback_data="GO"))

            training = "\n\t\t".join([x for x, y in current_dict.get("training").items() if y])
            list_user = "\n\t\t".join([x for x in current_dict.get("Users").keys()])
            await message.answer("РЕЗЮМЕ\n\n"
                                 "Цель обучения:\n\t\t{}\n"
                                 "Тема обучения:\n\t\t{}\n"
                                 "Выбранные виды обучения:\n\t\t{}\n"
                                 "У сотрудников:\n\t\t{}".format(
                                    current_dict.get("target"),
                                    current_dict.get("subject"),
                                    training,
                                    list_user), reply_markup=kb)


async def query_resume(query: types.CallbackQuery, state: FSMContext):
    if query.data == "GO":
        await query.message.delete()
        async with state.proxy() as data:
            current_dict: dict = data.get("Current proc")
            training = "\n\t\t".join([x for x, y in current_dict.get("training").items() if y])
            list_user = "\n\t\t".join([x for x in current_dict.get("Users").keys()])
            data["Current proc"]["time start"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            data["Current proc"]["time finish"] = 0
            data["Current proc"]["time start pause"] = 0
            data["Current proc"]["time finish pause"] = 0
            data["Current proc"]["time pause duration"] = 0
            data["Current proc"]["time duration"] = 0
            data["Current proc"]["time clear duration"] = 0
            data["Current proc"]["Records duration"] = 0
            data["Current proc"]["Records"] = []
            data["Current proc"]["Timer"] = True
            await query.message.answer("РЕЗЮМЕ\n\n"
                                       "Цель обучения:\n\t\t{}\n"
                                       "Тема обучения:\n\t\t{}\n"
                                       "Выбранные виды обучения:\n\t\t{}\n"
                                       "У сотрудников:\n\t\t{}".format(
                                        current_dict.get("target"),
                                        current_dict.get("subject"),
                                        training,
                                        list_user), reply_markup=ReplyKeyboardRemove())
        await FSMStudies.time.set()
        await query.message.answer("Обучение начало {}".format(datetime.now().strftime("%d.%m.%Y %H:%M:%S")))
        kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        kb.insert(InlineKeyboardButton(text="Пауза", callback_data="pause"))
        kb.insert(InlineKeyboardButton(text="Закончить обучение", callback_data="finish"))
        await query.message.answer("Идет процесс обучение:\n"
                                   "(пока таймер не завершен, вы можете отправлять звуковые сообщения с обучением) ",
                                   reply_markup=kb)
        await memory_bot.save_memory(state)
        await start_timer(query.message, state)
    elif query.data == "BACK":
        await query.message.answer("Напишите ФАМИЛИЮ обучаемого:", reply_markup=types.ReplyKeyboardRemove())
        async with state.proxy() as data:
            data["Current proc"] = {"Type": "Обучение", "Users": dict()}
        await state.set_state("FSMStudies:enter_family")
        await query.message.delete()
        await memory_bot.save_memory(state)


async def start_timer(message: types.Message, state: FSMContext):
    while True:
        async with state.proxy() as data:
            if data.get("Current proc") is not None:
                if data.get("Current proc").get("Timer") is not None:
                    await asyncio.sleep(60*30)
                    async with state.proxy() as data2:
                        if data2.get("Current proc") is not None:
                            if data2.get("Current proc").get("Timer") is not None:
                                msg = await message.answer("Напоминаю, что у вас идет обучение")
                                await asyncio.sleep(30)
                                await message.bot.delete_message(message.from_user.id, msg.message_id)
                else:
                    return
            else:
                return


async def my_time(query: types.CallbackQuery, state: FSMContext):
    if query.data == "finish":
        async with state.proxy() as data:
            data["Current proc"]["time finish"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            if data["Current proc"]["time start pause"] != 0:
                data["Current proc"]["time finish pause"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                data["Current proc"]["time pause duration"] = data["Current proc"]["time pause duration"] + (
                    datetime.strptime(data["Current proc"]["time finish pause"], "%d.%m.%Y %H:%M:%S") -
                    datetime.strptime(data["Current proc"]["time start pause"], "%d.%m.%Y %H:%M:%S")
                ).total_seconds()
                data["Current proc"]["time finish pause"] = 0
                data["Current proc"]["time start pause"] = 0
            data["Current proc"]["time duration"] = \
                (datetime.strptime(data["Current proc"]["time finish"], "%d.%m.%Y %H:%M:%S") -
                datetime.strptime(data["Current proc"]["time start"], "%d.%m.%Y %H:%M:%S")).total_seconds()
            data["Current proc"]["time clear duration"] = \
                data["Current proc"]["time duration"] - \
                data["Current proc"]["time pause duration"]
        await query.message.delete()
        await query.message.answer("Учет времени завершен {}".format(datetime.now().strftime("%d.%m.%Y %H:%M:%S")),
                                   reply_markup=ReplyKeyboardRemove())
        await query.message.answer("Введите оценку от 0 до 100", reply_markup=ReplyKeyboardRemove())
        await FSMStudies.grade.set()
        await memory_bot.save_memory(state)

    elif query.data == "pause":
        async with state.proxy() as data:
            data["Current proc"]["time start pause"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        await query.message.delete()
        kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        kb.insert(InlineKeyboardButton(text="Возобновить", callback_data="unpause"))
        kb.insert(InlineKeyboardButton(text="Закончить обучение", callback_data="finish"))
        await query.message.answer("Процесс обучение приостановлен: ", reply_markup=kb)
        await memory_bot.save_memory(state)
    elif query.data == "unpause":
        async with state.proxy() as data:
            data["Current proc"]["time finish pause"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            data["Current proc"]["time pause duration"] = data["Current proc"]["time pause duration"] + (
                datetime.strptime(data["Current proc"]["time finish pause"], "%d.%m.%Y %H:%M:%S") -
                datetime.strptime(data["Current proc"]["time start pause"], "%d.%m.%Y %H:%M:%S")
            ).total_seconds()
            data["Current proc"]["time finish pause"] = 0
            data["Current proc"]["time start pause"] = 0
        await query.message.delete()
        kb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        kb.insert(InlineKeyboardButton(text="Пауза", callback_data="pause"))
        kb.insert(InlineKeyboardButton(text="Закончить обучение", callback_data="finish"))
        await query.message.answer("Идет процесс обучение: ", reply_markup=kb)
        await memory_bot.save_memory(state)


async def grade(message: types.Message, state: FSMContext):
    try:
        if 0 <= int(message.text) <= 100:
            await message.answer("Введите комментарий, если требуется",
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Пропустить"))
            async with state.proxy() as data:
                data["Current proc"]["grade"] = message.text
            await FSMStudies.comment.set()
            await memory_bot.save_memory(state)
        else:
            await message.delete()
    except ValueError:
        await message.delete()


async def comment(message: types.Message, state: FSMContext):
    await message.answer("Введите информацию о дополнительном контроле, если требуется",
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Пропустить"))
    async with state.proxy() as data:
        data["Current proc"]["comment"] = message.text
    await FSMStudies.control.set()
    await memory_bot.save_memory(state)


async def control(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["Current proc"]["control"] = message.text
        data["Current proc"]["Timer"] = None
    await memory_bot.save_memory(state)
    await save_current_lesson(message=message, state=state)


async def save_current_lesson(message: types.Message, state: FSMContext):
    await message.answer("Сохраняю данные об обучении...", reply_markup=ReplyKeyboardRemove())
    async with state.proxy() as data:
        await message.answer(
            f"Обучение длилось: {str(data['Current proc']['time clear duration'] / 60).split('.')[0]} минут")
        if await save_learn_to_file(data):
            await message.answer("Данные успешно сохранены!", reply_markup=ReplyKeyboardRemove())
            await variants_actions(message=message, state=state)
        else:
            await message.answer("Не могу сохранить данные в папку, попробуй повторить позднее",
                                 reply_markup=ReplyKeyboardRemove())


async def save_audio(message: types.Message, state: FSMContext):
    try:
        file = await message.bot.get_file(message.voice.file_id)
        file = file.file_path
        path = os.sep * 2 + os.path.join("tg-storage01", "Служба персонала", "Общие", "Общая", "Обучение",
                                         "Сохраненные аудио от бота по обучению")
        async with state.proxy() as data:
            thema = data.get("Current proc").get("subject").replace(os.sep, "_")
        for word in thema:
            if not word.isalpha() and word != " ":
                thema = thema.replace(word, "")
        filial = data.get("User_filial")
        otdel = data.get("User_otdel")
        user = data.get("User")
        for word in filial:
            if not word.isalpha() and word != " ":
                filial = filial.replace(word, "")
        for word in otdel:
            if not word.isalpha() and word != " ":
                otdel = otdel.replace(word, "")
        for word in user:
            if not word.isalpha() and word != " ":
                user = user.replace(word, "")
        thema = thema[:20].strip() + "___ длит " + str(message.voice.duration) + " сек"
        path = os.path.join(path,
                            filial,
                            otdel,
                            user,
                            "{} от {}.mp3".format(thema, datetime.now().strftime("%d_%m_%Y %H_%M_%S"))
                            )
        async with state.proxy() as data:
            data["Current proc"]["Records"].append(path)
            data["Current proc"]["Records duration"] += message.voice.duration
        await memory_bot.save_memory(state)
        await message.bot.download_file(file, path)
        await message.delete()
        msg = await message.answer("Файл сохранен в папке")
        await asyncio.sleep(10)
        await message.bot.delete_message(message.from_user.id, msg.message_id)
    except Exception as error:
        msg = await message.answer("Не могу сохранить этот файл! "
                                   "Он слишком большой(больше 20 МБ) В будущим старайтесь записывать файлы поменьше"
                                   "\nЕсли он действительно важен и "
                                   "его нужно сохранить, отправьте файл аналитикам")
        await asyncio.sleep(10)
        await message.bot.delete_message(message.from_user.id, msg.message_id)


async def save_learn_to_file(data: dict) -> bool:
    for _ in range(20):
        try:
            path_to_total_file = os.sep * 2 + os.path.join("tg-storage01", "Аналитический отдел", "Проекты",
                                                           "Telegram Боты", "Бот по обучению V2", "Выгрузки", "Обучение",
                                                           "Данные об обучении {}.xlsx".format(
                                                               datetime.now().replace(day=1).strftime("%d.%m.%Y")))
            if os.path.exists(path_to_total_file):
                df = pd.read_excel(io=path_to_total_file, sheet_name="Данные", )
            else:
                df = pd.DataFrame()
                df["ФИО кто"] = ""
                df["Отдел кто"] = ""
                df["Подразделение кто"] = ""
                df["Количество обучаемых"] = ""
                df["ФИО кого"] = ""
                df["Отдел кого"] = ""
                df["Подразделение кого"] = ""
                df["Вид обучения"] = ""
                df["Тема обучения"] = ""
                df["Цель обучения"] = ""
                df["Оценка"] = ""
                df["Комментарий"] = ""
                df["Контроль"] = ""
                df["Дата"] = ""
                df["Время начала"] = ""
                df["Время конец"] = ""
                df["Длительность"] = ""
                df["Звуковые сообщения"] = ""
                df["Звуковые сообщения длительность"] = ""
            for men, about_men in data.get("Current proc").get("Users").items():
                df.loc[len(df)] = [data.get("User"),
                                   data.get("User_otdel"),
                                   data.get("User_filial"),
                                   1,
                                   men,
                                   about_men.get("User_otdel"),
                                   about_men.get("User_filial"),
                                   ", ".join([x for x, y in data.get("Current proc").get("training").items() if y]),
                                   data.get("Current proc").get("subject"),
                                   data.get("Current proc").get("target"),
                                   int(data.get("Current proc").get("grade")),
                                   data.get("Current proc").get("comment"),
                                   data.get("Current proc").get("control"),
                                   datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                                   data.get("Current proc").get("time start"),
                                   data.get("Current proc").get("time finish"),
                                   round(data.get("Current proc").get("time clear duration") /
                                         len(data.get("Current proc").get("Users"))),
                                   data.get("Current proc").get("Records"),
                                   round(data.get("Current proc").get("Records duration") /
                                         len(data.get("Current proc").get("Users")))
                                   ]
            with pd.ExcelWriter(path_to_total_file) as writer:
                df.to_excel(writer, sheet_name="Данные", index=False)
            return True
        except PermissionError:
            await asyncio.sleep(2)
            continue


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(enter_family, state=FSMStudies.enter_family)
    dp.register_message_handler(enter_family_select_num, state=FSMStudies.enter_family_select_num)

    dp.register_callback_query_handler(add_user_or_next_step, state=FSMStudies.add_user_or_next_step)
    dp.register_callback_query_handler(choice_train, state=FSMStudies.choice_train)

    dp.register_message_handler(enter_subject, state=FSMStudies.enter_subject)
    dp.register_message_handler(enter_target, state=FSMStudies.enter_target)

    dp.register_callback_query_handler(query_resume, state=FSMStudies.resume)
    dp.register_callback_query_handler(my_time, state=FSMStudies.time)
    dp.register_message_handler(save_audio, state=FSMStudies.time, content_types='voice')

    dp.register_message_handler(grade, state=FSMStudies.grade)
    dp.register_message_handler(comment, state=FSMStudies.comment)
    dp.register_message_handler(control, state=FSMStudies.control)
