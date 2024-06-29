from ..handlers.parse import name_parse
from aiogram import Bot,Router, F, types
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command
from aiogram.types.input_file import FSInputFile
import os
from datetime import datetime
from glob import glob
import openpyxl
import pandas as pd

from Telega.start_bot.keyboards.producer_kb import (role_kb, division_kb, brn_kb,center_kb, vybor_kb, mayma_kb,
                                                    bsk_kb, exit_but)
from Telega.start_bot.keyboards.maker_kb import (task_kb,brn_maker_kb,center_maker_kb,division_maker_kb,
                                                 bsk_maker_kb,mayma_maker_kb,vybor_maker_kb)


router = Router()
x = name_parse()
spis = []


class States(StatesGroup):
    fio_srch = State()
    choose_num = State()
    create_task = State()
    postanova_stat = State()
    maker_stat = State()
    get_task = State()
    choose_role = State()
    take_photo = State()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="👋 Добро пожаловать! Для начала тебе необходимо авторизоваться. Нажми на команду 👇 (/authorization)",
        reply_markup=ReplyKeyboardRemove()
    )
    if os.path.exists("../Отчет.xlsx"):
        pass
    else:
        filepath = "../Отчет.xlsx"
        wb = openpyxl.Workbook()
        wb.save(filepath)
        df = pd.DataFrame({"ID задания":[],
                           "Дата постановки задачи":[],
                           "Филиал":[],
                           "Секция":[],
                           "Постановщик":[],
                           "Отдел постановщика":[],
                           "Подразделение постановщика":[],
                           "Директория фото задания":[],
                           "Дата исполнения задания":[],
                           "Исполнитель":[],
                           "Отдел исполнителя":[],
                           "Подразделение исполнителя":[],
                           "Директория фото исполнения":[],
                           })
        df = df.reset_index(drop=True)
        df.to_excel(filepath)
@router.message(Command(commands=["authorization"]))
async def cmd_auth(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите часть своего ФИО, а я найду его в списке",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.fio_srch)

@router.message(States.fio_srch)
async def find_user(message:Message, state: FSMContext):

    u_message = message.text.lower()
    chat_id = message.chat.id
    matches = [name for name in x[0] if u_message in name.lower()]
    new_data= {str(index):name for index,name in enumerate(matches)}

    # for k in new_data.keys():
    #     print(len(str(new_data[k])))
    await state.update_data(**new_data)

    if matches:
        response_message = "\n" + "\n".join(f"{index + 1}. {name}" for index, name in enumerate(matches))

        await message.answer(response_message)
        await message.answer("Под каким ты номером?\n(введите число)")
        matches.clear()
    else:
        response_message = "Не могу найти тебя в списке :(попробуй ещё раз (/authorization) или приходи в другой раз (/stop)!"
        await message.answer(response_message)
        matches.clear()
    await state.set_state((States.choose_num))

@router.message(States.choose_num)
async def proof_user(message:Message, state: FSMContext):
    answ = message.text
    new_data = await state.get_data()

    check_list = [int(key) for key, values in new_data.items()]

    if int(answ)-1 in check_list:
        if int(answ) != 0:

            for key,values in new_data.items():

                if int(answ) == int(key) and int(key) != 0:

                    await message.answer(f"{new_data[str(int(key)-1)]}, вы постановщик или исполнитель?", reply_markup=role_kb)
                    filename = {"Fname": f"{new_data[str(int(key)-1)]}"}
                    filename["Only_name"] = new_data[str(int(key)-1)]
                    await state.update_data(filename)

                elif int(answ) == int(key)+1:

                    await message.answer(f"{new_data[str(int(key))]}, вы постановщик или исполнитель?",
                                         reply_markup=role_kb)
                    filename = {"Fname": f"{new_data[str(int(key))]}"}
                    filename["Only_name"] = new_data[str(int(key))]
                    await state.update_data(filename)
        elif answ.isalpha():
            await message.answer("Возможно, вы ввели не цифру. Попробуйте найти себя еще раз")
            await state.set_state((States.choose_num))
        elif int(answ) == 0:
            await message.answer("Возможно, произошла ошибка: попробуй ещё раз (/authorization)!")
    else:
        await message.answer("Вариант под этим номером отсутсвует. Попробуй еще раз (/authorization)")



@router.callback_query(F.data == "postanova")
async def choose_division(callback: types.CallbackQuery, state: FSMContext):
    os.makedirs("Фото от постановщика", exist_ok=True)
    id = {"id": 1}
    await state.update_data(id)
    await callback.message.answer("Выберите подразделение:", reply_markup=division_kb)
    await state.set_state(States.postanova_stat)

@router.callback_query(F.data =='Центральный офис')
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = {"Path": f"Фото от постановщика/Центральный офис"}
    await state.update_data(path)
    fname = await state.get_data()
    filename = fname["Fname"]
    fname = {"Fname": f"Центральный офис_({filename}"}
    await state.update_data(fname)
    os.makedirs(f"Фото от постановщика/Центральный офис", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup=center_kb)

@router.callback_query(F.data == "Филиал Выбор")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = {"Path": f"Фото от постановщика/Филиал Выбор"}
    await state.update_data(path)
    fname = await state.get_data()
    filename = fname["Fname"]
    fname = {"Fname": f"Филиал Выбор_({filename}"}
    await state.update_data(fname)
    os.makedirs(f"Фото от постановщика/Филиал Выбор", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup=vybor_kb)

@router.callback_query(F.data == "Филиал Барнаул")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = {"Path": f"Фото от постановщика/Филиал Барнаул"}
    await state.update_data(path)
    fname = await state.get_data()
    filename = fname["Fname"]
    fname = {"Fname": f"Филиал Барнаул_({filename}"}
    await state.update_data(fname)
    os.makedirs(f"Фото от постановщика/Филиал Барнаул", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup=brn_kb)

@router.callback_query(F.data == "Филиал Бийск")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = {"Path": f"Фото от постановщика/Филиал Бийск"}
    await state.update_data(path)
    fname = await state.get_data()
    filename = fname["Fname"]
    fname = {"Fname": f"Филиал Бийск_({filename}"}
    await state.update_data(fname)
    os.makedirs(f"Фото от постановщика/Филиал Бийск", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup=bsk_kb)

@router.callback_query(F.data == "Филиал Майма")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = {"Path": f"Фото от постановщика/Филиал Майма"}
    await state.update_data(path)
    fname = await state.get_data()
    filename = fname["Fname"]
    fname = {"Fname": f"Филиал Майма_({filename}"}
    await state.update_data(fname)
    os.makedirs(f"Фото от постановщика/Филиал Майма", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup= mayma_kb)


@router.callback_query(F.data == "Секция A")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = await state.get_data()
    os.makedirs(f"{path['Path']}/Секция A", exist_ok=True)
    path = {"Section":f"{path['Path']}/Секция A"}
    await state.update_data(path)
    await callback.message.answer("Прикрепите фотографию:", reply_markup=exit_but)
    await state.set_state((States.create_task))

@router.callback_query(F.data == "Секция В")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = await state.get_data()
    os.makedirs(f"{path['Path']}/Секция В", exist_ok=True)
    path = {"Section": f"{path['Path']}/Секция В"}
    await state.update_data(path)
    await callback.message.answer("Прикрепите фотографию:", reply_markup=exit_but)
    await state.set_state((States.create_task))

@router.callback_query(F.data == "Секция Д")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = await state.get_data()
    os.makedirs(f"/{path['Path']}/Секция Д", exist_ok=True)
    path = {"Section": f"/{path['Path']}/Секция Д"}
    await state.update_data(path)
    await callback.message.answer("Прикрепите фотографию:", reply_markup=exit_but)
    await state.set_state((States.create_task))

@router.callback_query(F.data == "Секция М")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = await state.get_data()
    os.makedirs(f"{path['Path']}/Секция М", exist_ok=True)
    path = {"Section": f"{path['Path']}/Секция М"}
    await state.update_data(path)
    await callback.message.answer("Прикрепите фотографию:", reply_markup=exit_but)
    await state.set_state((States.create_task))

@router.callback_query(F.data == "Секция С")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = await state.get_data()
    os.makedirs(f"{path['Path']}/Секция С", exist_ok=True)
    path = {"Section": f"{path['Path']}/Секция С"}
    dest = path["Section"]
    photo = {f"{dest}": []}
    await state.update_data(path)
    await state.update_data(photo)
    await callback.message.answer("Прикрепите фотографию:", reply_markup=exit_but)
    await state.set_state((States.create_task))

@router.message(States.create_task, F.photo)
async def create_task(message: types.Message, state: FSMContext):
    path = await state.get_data()

    unix_date = message.date
    date = unix_date.strftime("%Y.%m.%d")
    time = datetime.now().strftime("%H-%M-%S")
    dest = path["Section"]
    name = path["Fname"]
    files_quant = len(glob(f"{dest}/*"))
    print(f"{dest}/*")
    print(glob(f"{dest}/*"))
    print(files_quant)
    await message.bot.download(file=message.photo[-1], destination=f"{dest}/{date} {time}_{name}_id={files_quant}).jpg")

    # Чтение данных из Excel файла
    df = pd.read_excel("../Отчет.xlsx")

    remove_list =  [el for el in df.columns if "Unnamed" in el]
    if len(remove_list) != 0:
        for el in remove_list:
            df.drop(columns=el, errors='ignore')
    # Создаем новую строку для добавления
    new_row = {
        "ID задания": files_quant,
        "Дата постановки задачи": f"{date} {time}",
        "Филиал": dest.split("/")[1],
        "Секция": dest.split("/")[2],
        "Постановщик": path["Only_name"],
        "Отдел постановщика": x[1][x[0].index(path["Only_name"])],
        "Подразделение постановщика": x[2][x[0].index(path["Only_name"])],
        "Директория фото задания": f"{dest}/{date} {time}_{name}_id={files_quant}).jpg"
    }

    # Добавляем новую строку в DataFrame
    df = df._append(new_row, ignore_index=True)

    # Записываем DataFrame обратно в файл
    df.to_excel("../Отчет.xlsx", index=False)

    await message.answer("Отлично. Фото сохранено. Можно прикрепить следующее задание")


@router.message(F.text == "Выйти")
async def exit_event(message: types.Message, state: FSMContext):
    await message.answer("Задание сохранено")
    datas = await state.get_data()
    if datas["Path"].split("/")[1] == 'Центральный офис':
        await message.answer("Выберите секцию:", reply_markup=center_kb)
    if datas["Path"].split("/")[1] == 'Филиал Барнаул':
        await message.answer("Выберите секцию:", reply_markup=brn_kb)
    if datas["Path"].split("/")[1] == 'Филиал Бийск':
        await message.answer("Выберите секцию:", reply_markup=bsk_kb)
    if datas["Path"].split("/")[1] == 'Филиал Майма':
        await message.answer("Выберите секцию:", reply_markup=mayma_kb)
    if datas["Path"].split("/")[1] == 'Филиал Выбор':
        await message.answer("Выберите секцию:", reply_markup=vybor_kb)
    await message.answer("Вы постановщик или исполнитель? Нажмите (/authorization) если хотите выбрать пользователя", reply_markup=role_kb)


"ветка исполнителя"
@router.callback_query(F.data == "ispolnitel")
async def choose_division(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите подразделение:", reply_markup=division_maker_kb)
    await state.set_state(States.maker_stat)

@router.callback_query(F.data =='ЦО')
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите секцию:", reply_markup=center_maker_kb)
    div_name = {"Отдел": 'Центральный офис'}
    await state.update_data(div_name)

@router.callback_query(F.data =='Выбор')
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите секцию:", reply_markup=center_maker_kb)
    div_name = {"Отдел": 'Филиал Выбор'}
    await state.update_data(div_name)

@router.callback_query(F.data =='Барнаул')
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите секцию:", reply_markup=center_maker_kb)
    div_name = {"Отдел": 'Филиал Барнаул'}
    await state.update_data(div_name)

@router.callback_query(F.data =='Бийск')
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите секцию:", reply_markup=center_maker_kb)
    div_name = {"Отдел": 'Филиал Бийск'}
    await state.update_data(div_name)

@router.callback_query(F.data =='Майма')
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите секцию:", reply_markup=center_maker_kb)
    div_name = {"Отдел": 'Филиал Майма'}
    await state.update_data(div_name)


@router.message(F.text == "А")
async def choose_sec1(message: types.Message, state: FSMContext):
    path = await state.get_data()

    sec_part = {"Подотдел":f'\\{path["Отдел"]}\\Секция A'}
    await state.update_data(sec_part)
    strg = await state.get_data()
    dir_path1 = strg["Подотдел"]
    photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
    index = 0
    strg["Savepath"] = photo[:-1]
    strg["index"] = index
    await state.update_data(strg)
    direktor = glob(photo, recursive=True)

    if len(direktor)!=0:
        document = FSInputFile(direktor[0])
        bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
        await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
    else:
        await message.answer('В этом подразделении задач нет')

@router.message(F.text == "В")
async def choose_sec1(message: types.Message, state: FSMContext):
    path = await state.get_data()

    sec_part = {"Подотдел":f'\\{path["Отдел"]}\\Секция В'}
    await state.update_data(sec_part)
    strg = await state.get_data()
    dir_path1 = strg["Подотдел"]
    photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
    index = 0
    strg["Savepath"] = photo[:-1]
    strg["index"] = index
    await state.update_data(strg)
    direktor = glob(photo, recursive=True)

    if len(direktor)!=0:
        document = FSInputFile(direktor[0])
        bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
        await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
    else:
        await message.answer('В этом подразделении задач нет')

    @router.message(F.text == "Д")
    async def choose_sec1(message: types.Message, state: FSMContext):
        path = await state.get_data()

        sec_part = {"Подотдел": f'\\{path["Отдел"]}\\Секция Д'}
        await state.update_data(sec_part)
        strg = await state.get_data()
        dir_path1 = strg["Подотдел"]
        photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
        index = 0
        strg["Savepath"] = photo[:-1]
        strg["index"] = index
        await state.update_data(strg)
        direktor = glob(photo, recursive=True)

        if len(direktor) != 0:
            document = FSInputFile(direktor[0])
            bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
            await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
        else:
            await message.answer('В этом подразделении задач нет')

@router.message(F.text == "М")
async def choose_sec1(message: types.Message, state: FSMContext):
    path = await state.get_data()

    sec_part = {"Подотдел":f'\\{path["Отдел"]}\\Секция М'}
    await state.update_data(sec_part)
    strg = await state.get_data()
    dir_path1 = strg["Подотдел"]
    photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
    index = 0
    strg["Savepath"] = photo[:-1]
    strg["index"] = index
    await state.update_data(strg)
    direktor = glob(photo, recursive=True)

    if len(direktor)!=0:
        document = FSInputFile(direktor[0])
        bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
        await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
    else:
        await message.answer('В этом подразделении задач нет')

@router.message(F.text == "С")
async def choose_sec1(message: types.Message, state: FSMContext):
    path = await state.get_data()

    sec_part = {"Подотдел":f'\\{path["Отдел"]}\\Секция С'}
    await state.update_data(sec_part)
    strg = await state.get_data()
    dir_path1 = strg["Подотдел"]
    photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
    index = 0
    strg["Savepath"] = photo[:-1]
    strg["index"] = index
    await state.update_data(strg)
    direktor = glob(photo, recursive=True)

    if len(direktor)!=0:
        document = FSInputFile(direktor[0])
        bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
        await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
    else:
        await message.answer('В этом подразделении задач нет')
@router.callback_query(F.data == "ready")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Принято. Отправьте фотоотчет")
    await state.set_state((States.take_photo))


@router.message(States.take_photo, F.photo)
async def ispravlenie(message: types.Message, state: FSMContext):
    path = await state.get_data()
    unix_date = message.date
    date = unix_date.strftime("%Y.%m.%d")
    time = datetime.now().strftime("%H-%M-%S")
    dest = path["Savepath"].replace("Фото от постановщика", "Фото от исполнителя")
    name = path["Fname"]
    file_ex = glob(f"{dest}")
    file_id = len(file_ex)

    os.makedirs(f"{dest}", exist_ok=True)
    await message.bot.download(file=message.photo[-1], destination=f"{dest}/{date} {time}_{name}_id={file_id}.jpg")

    df = pd.read_excel("../Отчет.xlsx")

    df.loc[
        (df["Дата постановки задачи"] == (glob(path["Savepath"] + "*")[path["index"]]).split("\\")[-1].split("_")[0]),
        "Дата исполнения задания"] = f"{date} {time}"
    df.loc[
        (df["Дата постановки задачи"] == (glob(path["Savepath"] + "*")[path["index"]]).split("\\")[-1].split("_")[0]),
        "Исполнитель"] = path["Only_name"]
    df.loc[
        (df["Дата постановки задачи"] == (glob(path["Savepath"] + "*")[path["index"]]).split("\\")[-1].split("_")[0]),
        "Отдел исполнителя"] = x[1][x[0].index(path["Only_name"])]
    df.loc[
        (df["Дата постановки задачи"] == (glob(path["Savepath"] + "*")[path["index"]]).split("\\")[-1].split("_")[0]),
        "Подразделение исполнителя"] = x[2][x[0].index(path["Only_name"])]
    df.loc[
        (df["Дата постановки задачи"] == (glob(path["Savepath"] + "*")[path["index"]]).split("\\")[-1].split("_")[0]),
        "Директория фото исполнения"] = f"{dest}/{date} {time}_{name}_id={file_id}.jpg"
    df.to_excel("../Отчет.xlsx")
    os.remove((glob(path["Savepath"]+"*")[path["index"]]))
    await message.answer("Отлично. Фото сохранено")
    if glob(f"{dest}") != 0:
        await state.set_state((States.get_task))
    else:
        await message.answer('В этом подразделении задач нет')
    # dir_path1 = path["Подотдел"]
    # photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
    # path["Savepath"] = photo[:-1]
    # index = path["index"]
    #
    #
    # await state.update_data(path)
    # direktor = glob(photo, recursive=True)
    #
    # if len(direktor) != 0:
    #
    #     document = FSInputFile(direktor[index])
    #     bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
    #     await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
    # else:
    #     await message.answer('В этом подразделении задач нет')

@router.callback_query(F.data == "next")
async def create_task(callback: types.CallbackQuery, state: FSMContext):

    strg = await state.get_data()
    dir_path1 = strg["Подотдел"]
    photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
    strg["Savepath"] = photo[:-1]
    index = strg["index"] + 1
    strg["index"] = index

    await state.update_data(strg)
    direktor = glob(photo, recursive=True)

    if len(direktor) != 0 and index <= len(direktor) - 1:

        document = FSInputFile(direktor[index])
        bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
        await bot.send_document(chat_id=callback.message.chat.id, document=document, reply_markup=task_kb)
    else:
        await callback.message.answer('В этом подразделении задач нет')

@router.callback_query(F.data == "exit")
async def exit(callback: types.CallbackQuery, state: FSMContext):
    datas = await state.get_data()
    if datas["Отдел"] == 'Центральный офис':
        await callback.message.answer("Выберите секцию:", reply_markup=center_maker_kb)
    if datas["Отдел"] == 'Филиал Барнаул':
        await callback.message.answer("Выберите секцию:", reply_markup=brn_maker_kb)
    if datas["Отдел"] == 'Филиал Бийск':
        await callback.message.answer("Выберите секцию:", reply_markup=bsk_maker_kb)
    if datas["Отдел"] == 'Филиал Майма':
        await callback.message.answer("Выберите секцию:",reply_markup=mayma_maker_kb)
    if datas["Отдел"] == 'Филиал Выбор':
        await callback.message.answer("Выберите секцию:",reply_markup=vybor_maker_kb)
    await callback.message.answer("Вы постановщик или исполнитель? Нажмите (/authorization) если хотите выбрать пользователя",
                         reply_markup=role_kb)




















