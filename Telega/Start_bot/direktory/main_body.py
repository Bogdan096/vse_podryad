#импорт библиотек
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

'''импорт клавиатур'''
from Telega.start_bot.keyboards.producer_kb import (role_kb, division_kb, brn_kb, center_kb, vybor_kb, mayma_kb,
                                                    bsk_kb, exit_but, brn_prod_kb, center_prod_kb, vybor_prod_kb,
                                                    mayma_prod_kb, bsk_prod_kb)
from Telega.start_bot.keyboards.maker_kb import (task_kb,brn_maker_kb,center_maker_kb,division_maker_kb,
                                                 bsk_maker_kb,mayma_maker_kb,vybor_maker_kb)

slovarik = {}
router = Router()
x = name_parse()
spis = []


class States(StatesGroup):
    fio_srh = State()
    chose_num = State()
    create_task = State()
    postanova_stat = State()
    maker_stat = State()
    get_task = State()
    choose_role = State()
    take_photo = State()
    get_list_of_task = State()
    extra_state = State()

'''хэндлер команды старт'''
@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="👋 Добро пожаловать! Для начала тебе необходимо авторизоваться. Нажми на команду 👇 (/authorization)",
        reply_markup=ReplyKeyboardRemove()
    )
    '''проверка существования файла с отчетом, если нет то создаем его со следующими колонками'''
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


'''хэндлер команды авторизация'''
@router.message(Command(commands=["authorization"]))
async def cmd_auth(message: Message, state: FSMContext):
    await state.clear()
    '''сообщение с запросом фио'''
    await message.answer("Введите часть своего ФИО, а я найду его в списке",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.fio_srh)

'''хэндлер поиска сотруднка по фио'''
@router.message(States.fio_srh)
async def find_user(message:Message, state: FSMContext):

    u_message = message.text.lower()
    chat_id = message.chat.id
    '''создаем список и словарь с подходящими сотрудниками по ФИО'''
    matches = [name for name in x[0] if u_message in name.lower()]
    new_data= {str(index):name for index,name in enumerate(matches)}

    # for k in new_data.keys():
    #     print(len(str(new_data[k])))
    await state.update_data(**new_data)
    '''вывод сообщения с подходящими вариантами по номерам'''
    if matches:
        response_message = "\n" + "\n".join(f"{index + 1}. {name}" for index, name in enumerate(matches))
        await message.answer(response_message)
        await message.answer("Под каким вы номером?\n(введите число)")
        matches.clear()
    else:
        response_message = "Не могу найти вас в списке :(попробуй ещё раз (/authorization) или приходите в другой раз (/stop)!"
        await message.answer(response_message)
        matches.clear()
    await state.set_state((States.chose_num))

'''хэндлер выбора сотрудника'''
@router.message(States.chose_num)
async def zalupa(message:Message, state: FSMContext):
    check_list = []
    alpha_list=[]
    answ = message.text
    new_data = await state.get_data()
    '''заполнение словаря только цифровыми ключами'''
    for key, val in new_data.items():
        if key.isdigit():
            check_list.append(int(key))
        else:
            alpha_list.append(key)
    '''выдача пользователю сообщения с выбранным вариантом'''
    if answ.isdigit():
        if int(answ)-1 in check_list:
            if int(answ) != 0:

                for key,values in new_data.items():

                    if int(answ) == int(key) and int(key) != 0:

                        await message.answer(f"{new_data[str(int(key)-1)]}, вы постановщик или исполнитель?", reply_markup=role_kb)

                        filename = {"Fname": f"{new_data[str(int(key)-1)]}"}
                        filename["Only_name"] = new_data[str(int(key)-1)]
                        filename["Division"] = x[2][x[0].index(new_data[str(int(key) - 1)])]
                        filename["Subdivision"] = x[1][x[0].index(new_data[str(int(key) - 1)])]
                        await state.update_data(filename)

                        '''выдача пользователю сообщения с выбранным вариантом, если вариант был 1'''
                    elif int(answ) == int(key)+1:

                        await message.answer(f"{new_data[str(int(key))]}, вы постановщик или исполнитель?",
                                             reply_markup=role_kb)


                        filename = {"Fname": f"{new_data[str(int(key))]}"}
                        filename["Only_name"] = new_data[str(int(key))]
                        filename["Division"] = x[2][x[0].index(new_data[str(int(key))])]
                        filename["Subdivision"] = x[1][x[0].index(new_data[str(int(key))])]
                        await state.update_data(filename)
            elif answ.isalpha():
                await message.answer("Возможно, вы ввели не цифру. Попробуйте найти себя еще раз")

            elif int(answ) == 0:
                await message.answer("Возможно, произошла ошибка: попробуйте ещё раз (/authorization)!")
        else:
            await message.answer("Вариант под этим номером отсутствует. Попробуйте еще раз (/authorization)")



'''хэндлер роли Постановщик'''
@router.callback_query(F.data == "postanova")
async def choose_division(callback: types.CallbackQuery, state: FSMContext):
    '''создание директории для постановщика и выбор подразделения с клавиатурой'''
    os.makedirs("Фото от постановщика", exist_ok=True)
    id = {"id": 1}
    await state.update_data(id)
    await callback.message.answer("Выберите подразделение:", reply_markup=division_kb)
    await state.set_state(States.postanova_stat)

'''если выбран Центральный офис'''
@router.callback_query(F.data =='Центральный офис')
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    '''создание директории и запись в словарь для формирования отчета'''
    path = {"Path": f"Фото от постановщика/Центральный офис"}
    path["Регион"] = "Центральный офис"
    await state.update_data(path)
    fname = await state.get_data()
    filename = fname["Fname"]

    '''формирование имени файла'''
    fname = {"Fname": f"Центральный офис_({filename}"}
    await state.update_data(fname)
    os.makedirs(f"Фото от постановщика/Центральный офис", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup=center_prod_kb)

'''если выбран Выбор'''
@router.callback_query(F.data == "Филиал Выбор")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    '''создание директории и запись в словарь для формирования отчета'''
    path = {"Path": f"Фото от постановщика/Филиал Выбор"}
    path["Регион"] = "Выбор"
    await state.update_data(path)
    fname = await state.get_data()
    filename = fname["Fname"]
    '''формирование имени файла'''
    fname = {"Fname": f"Филиал Выбор_({filename}"}
    await state.update_data(fname)
    os.makedirs(f"Фото от постановщика/Филиал Выбор", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup=vybor_prod_kb)

'''если выбран Барнаул'''
@router.callback_query(F.data == "Филиал Барнаул")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    '''создание директории и запись в словарь для формирования отчета'''
    path = {"Path": f"Фото от постановщика/Филиал Барнаул"}
    path["Регион"] = "Барнаул"
    await state.update_data(path)
    fname = await state.get_data()
    filename = fname["Fname"]
    '''формирование имени файла'''
    fname = {"Fname": f"Филиал Барнаул_({filename}"}
    await state.update_data(fname)
    os.makedirs(f"Фото от постановщика/Филиал Барнаул", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup=brn_prod_kb)

'''если выбран Бийск'''
@router.callback_query(F.data == "Филиал Бийск")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    '''создание директории и запись в словарь для формирования отчета'''
    path = {"Path": f"Фото от постановщика/Филиал Бийск"}
    path["Регион"] = "Бийск"
    await state.update_data(path)
    fname = await state.get_data()
    filename = fname["Fname"]
    '''формирование имени файла'''
    fname = {"Fname": f"Филиал Бийск_({filename}"}
    await state.update_data(fname)
    os.makedirs(f"Фото от постановщика/Филиал Бийск", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup=bsk_prod_kb)

'''если выбрана Майма'''
@router.callback_query(F.data == "Филиал Майма")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    '''создание директории и запись в словарь для формирования отчета'''
    path = {"Path": f"Фото от постановщика/Филиал Майма"}
    path["Регион"]= "Майма"
    await state.update_data(path)
    fname = await state.get_data()
    filename = fname["Fname"]
    '''формирование имени файла'''
    fname = {"Fname": f"Филиал Майма_({filename}"}
    await state.update_data(fname)
    os.makedirs(f"Фото от постановщика/Филиал Майма", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup= mayma_prod_kb)


@router.message(F.text == "Секция А")
async def choose_sec1(message: types.Message, state: FSMContext):
    '''создание директории и запись в словарь для формирования отчета'''
    path = await state.get_data()
    os.makedirs(f"{path['Path']}/Секция А", exist_ok=True)
    rg = path["Регион"]
    path = {"Section":f"{path['Path']}/Секция А"}
    await state.update_data(path)
    '''вывод клавиатуры, соответствующей выбранному филиалу'''
    if rg == "Центральный офис":
        await message.answer("Прикрепите одну фотографию:", reply_markup=center_prod_kb)

        await state.set_state((States.create_task))
    if rg == "Барнаул":
        await message.answer("Прикрепите одну фотографию:", reply_markup=brn_prod_kb)

        await state.set_state((States.create_task))
    if rg == "Бийск":
        await message.answer("Прикрепите одну фотографию:", reply_markup=bsk_prod_kb)

        await state.set_state((States.create_task))
    if rg == "Майма":
        await message.answer("Прикрепите одну фотографию:", reply_markup=mayma_prod_kb)

        await state.set_state((States.create_task))
    if rg == "Выбор":
        await message.answer("Прикрепите одну фотографию:", reply_markup=vybor_prod_kb)

        await state.set_state((States.create_task))

@router.message(F.text == "Секция В")
async def choose_sec1(message: types.Message, state: FSMContext):
    '''создание директории и запись в словарь для формирования отчета'''
    path = await state.get_data()
    os.makedirs(f"{path['Path']}/Секция В", exist_ok=True)
    rg = path["Регион"]
    path = {"Section": f"{path['Path']}/Секция В"}
    await state.update_data(path)
    '''вывод клавиатуры, соответствующей выбранному филиалу'''
    if rg == "Центральный офис":
        await message.answer("Прикрепите одну фотографию:", reply_markup=center_prod_kb)
        await state.set_state((States.create_task))
    if rg == "Барнаул":
        await message.answer("Прикрепите одну фотографию:", reply_markup=brn_prod_kb)
        await state.set_state((States.create_task))
    if rg == "Бийск":
        await message.answer("Прикрепите одну фотографию:", reply_markup=bsk_prod_kb)
        await state.set_state((States.create_task))
    if rg == "Майма":
        await message.answer("Прикрепите одну фотографию:", reply_markup=mayma_prod_kb)
        await state.set_state((States.create_task))
    if rg == "Выбор":
        await message.answer("Прикрепите одну фотографию:", reply_markup=vybor_prod_kb)
        await state.set_state((States.create_task))

@router.message(F.text == "Секция Д")
async def choose_sec1(message: types.Message, state: FSMContext):
    '''создание директории и запись в словарь для формирования отчета'''
    path = await state.get_data()
    os.makedirs(f"{path['Path']}/Секция Д", exist_ok=True)
    rg = path["Регион"]
    path = {"Section": f"{path['Path']}/Секция Д"}
    await state.update_data(path)
    '''вывод клавиатуры, соответствующей выбранному филиалу'''
    if rg == "Центральный офис":
        await message.answer("Прикрепите одну фотографию:", reply_markup=center_prod_kb)
        await state.set_state((States.create_task))
    if rg == "Барнаул":
        await message.answer("Прикрепите одну фотографию:", reply_markup=brn_prod_kb)
        await state.set_state((States.create_task))
    if rg == "Бийск":
        await message.answer("Прикрепите одну фотографию:", reply_markup=bsk_prod_kb)
        await state.set_state((States.create_task))
    if rg == "Майма":
        await message.answer("Прикрепите одну фотографию:", reply_markup=mayma_prod_kb)
        await state.set_state((States.create_task))
    if rg == "Выбор":
        await message.answer("Прикрепите одну фотографию:", reply_markup=vybor_prod_kb)
        await state.set_state((States.create_task))

@router.message(F.text == "Секция М")
async def choose_sec1(message: types.Message, state: FSMContext):
    '''создание директории и запись в словарь для формирования отчета'''
    path = await state.get_data()
    rg = path["Регион"]
    os.makedirs(f"{path['Path']}/Секция М", exist_ok=True)
    path = {"Section": f"{path['Path']}/Секция М"}
    await state.update_data(path)
    '''вывод клавиатуры, соответствующей выбранному филиалу'''
    if rg == "Центральный офис":
        await message.answer("Прикрепите одну фотографию:", reply_markup=center_prod_kb)
        await state.set_state((States.create_task))
    if rg == "Барнаул":
        await message.answer("Прикрепите одну фотографию:", reply_markup=brn_prod_kb)
        await state.set_state((States.create_task))
    if rg == "Бийск":
        await message.answer("Прикрепите одну фотографию:", reply_markup=bsk_prod_kb)
        await state.set_state((States.create_task))
    if rg == "Майма":
        await message.answer("Прикрепите одну фотографию:", reply_markup=mayma_prod_kb)
        await state.set_state((States.create_task))
    if rg == "Выбор":
        await message.answer("Прикрепите одну фотографию:", reply_markup=vybor_prod_kb)
        await state.set_state((States.create_task))

@router.message(F.text == "Секция С" )
async def choose_sec1(message: types.Message, state: FSMContext):
    '''создание директории и запись в словарь для формирования отчета'''
    path = await state.get_data()
    os.makedirs(f"{path['Path']}/Секция С", exist_ok=True)
    rg = path["Регион"]
    path = {"Section": f"{path['Path']}/Секция С"}
    dest = path["Section"]
    photo = {f"{dest}": []}
    await state.update_data(path)
    await state.update_data(photo)
    '''вывод клавиатуры, соответствующей выбранному филиалу'''
    if rg == "Центральный офис":
        await message.answer("Прикрепите одну фотографию:", reply_markup=center_prod_kb)

        await state.set_state((States.create_task))
    if rg == "Барнаул":
        await message.answer("Прикрепите одну фотографию:", reply_markup=brn_prod_kb)

        await state.set_state((States.create_task))
    if rg == "Бийск":
        await message.answer("Прикрепите одну фотографию:", reply_markup=bsk_prod_kb)

        await state.set_state((States.create_task))
    if rg == "Майма":
        await message.answer("Прикрепите одну фотографию:", reply_markup=mayma_prod_kb)

        await state.set_state((States.create_task))
    if rg == "Выбор":
        await message.answer("Прикрепите одну фотографию:", reply_markup=vybor_prod_kb)

        await state.set_state((States.create_task))

'''постановка задачи'''
@router.message(States.create_task, F.photo)
async def create_task(message: types.Message, state: FSMContext):

    path = await state.get_data()
    '''получение даты и времени постановки задачи'''
    unix_date = message.date
    date = unix_date.strftime("%Y.%m.%d")
    time = datetime.now().strftime("%H-%M-%S")
    dest = path["Section"]
    name = path["Fname"]
    files_quant = len(glob(f"{dest}/*"))
    '''сохранение фото в заранее созданную директорию'''
    await message.bot.download(file=message.photo[-1], destination=f"{dest}/{date} {time}_{name}_id={files_quant}).jpg")

    # Чтение данных из Excel файла
    df = pd.read_excel("../Отчет.xlsx",index_col=0)


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

    remove_list = [el for el in df.columns if "Unnamed" in el]
    if len(remove_list) != 0:
        for el in remove_list:
            df.drop(columns=el, errors='ignore')
    # Записываем DataFrame обратно в файл
    df.to_excel("../Отчет.xlsx", index=False)

    datas = await state.get_data()

    # вывод клавиатуры в зависимости от  ранее выбранного филиала
    if datas["Path"].split("/")[1] == 'Центральный офис':
        await message.answer("Отлично. Фото сохранено. Можно прикрепить следующее задание", reply_markup=center_prod_kb)
    if datas["Path"].split("/")[1] == 'Филиал Барнаул':
        await message.answer("Отлично. Фото сохранено. Можно прикрепить следующее задание", reply_markup=brn_prod_kb)
    if datas["Path"].split("/")[1] == 'Филиал Бийск':
        await message.answer("Отлично. Фото сохранено. Можно прикрепить следующее задание", reply_markup=bsk_prod_kb)
    if datas["Path"].split("/")[1] == 'Филиал Майма':
        await message.answer("Отлично. Фото сохранено. Можно прикрепить следующее задание", reply_markup=mayma_prod_kb)
    if datas["Path"].split("/")[1] == 'Филиал Выбор':
        await message.answer("Отлично. Фото сохранено. Можно прикрепить следующее задание", reply_markup=vybor_prod_kb)

# хэндлер кнопки Выйти
@router.message(F.text == "Выйти")
async def exit_event(message: types.Message, state: FSMContext):
    await message.answer("Задание сохранено")

    await message.answer("Вы постановщик или исполнитель? Нажмите (/authorization) если хотите выбрать пользователя", reply_markup=role_kb)


"ветка исполнителя"
@router.callback_query(F.data == "ispolnitel")
async def choose_division(callback: types.CallbackQuery, state: FSMContext):

    slovo = await state.get_data()
    # Проверяем есть ли в словаре данные о подразделении исполнителя
    if "Division" in slovo.keys():
        user_div = slovo["Division"]
    else:
        user_div = slovo["Подотдел"]
    # Формирование нвоого словаря
    sec_part = {"Подотдел": f'\\{user_div}'}
    sec_part["Fname"] = slovo["Fname"]
    sec_part["Only_name"] = slovo["Only_name"]

    # Вывод клавиатуры выбора секции в зависимости от Подразделения пользователя
    if "Центральный" in user_div:
        await callback.message.answer("Выберите секцию:", reply_markup=center_maker_kb)
        await state.clear()
        await state.set_state(States.extra_state)
        await state.update_data(sec_part)
    if "Барнаул" in user_div:
        await callback.message.answer("Выберите секцию:", reply_markup=brn_maker_kb)
        await state.clear()
        await state.set_state(States.extra_state)
        await state.update_data(sec_part)
    if "Бийск" in user_div:
        await callback.message.answer("Выберите секцию:", reply_markup=bsk_maker_kb)
        await state.clear()
        await state.set_state(States.extra_state)
        await state.update_data(sec_part)
    if "Выбор" in user_div:
        await callback.message.answer("Выберите секцию:", reply_markup=vybor_maker_kb)
        await state.clear()
        await state.set_state(States.extra_state)
        await state.update_data(sec_part)
    if "Майма" in user_div:
        await callback.message.answer("Выберите секцию:", reply_markup=mayma_maker_kb)
        await state.clear()
        await state.set_state(States.extra_state)
        await state.update_data(sec_part)

# Если выбрана секция А
@router.message(F.text == "А")
async def choose_division(message: types.Message, state: FSMContext):
    # Формирование директории для Исполнителя
        strg = await state.get_data()
        dir_path1 = strg["Подотдел"]+"\\Секция А"
        undersec = "\\Секция А"
        photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
        index = 0
        strg["Savepath"] = photo[:-1]
        strg["index"] = index
        strg["Подсекция"] = undersec
        await state.update_data(strg)
        direktor = glob(photo, recursive=True)

        #В зависимости от Подразделения исполнителя, вывод фото задач, хранящихся в соответствующей директории или соответсвующего сообщения, если директория пуста
        if "Центральный" in strg["Подотдел"]:
            if len(direktor)==0:
                await message.answer('В этой секции задач нет', reply_markup=center_maker_kb)
            else:
                while len(direktor)!=0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=center_maker_kb)
        if "Барнаул" in strg["Подотдел"]:
            if len(direktor)==0:
                await message.answer('В этой секции задач нет', reply_markup=brn_maker_kb)
            else:
                while len(direktor)!=0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=brn_maker_kb)
        if "Бийск" in strg["Подотдел"]:
            if len(direktor)==0:
                await message.answer('В этой секции задач нет', reply_markup=bsk_maker_kb)
            else:
                while len(direktor)!=0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=bsk_maker_kb)
        if "Выбор" in strg["Подотдел"]:
            if len(direktor)==0:
                await message.answer('В этой секции задач нет', reply_markup=vybor_maker_kb)
            else:
                while len(direktor)!=0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=vybor_maker_kb)
        if "Майма" in strg["Подотдел"]:
            if len(direktor)==0:
                await message.answer('В этой секции задач нет', reply_markup=mayma_maker_kb)
            else:
                while len(direktor)!=0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=mayma_maker_kb)

# Если выбрана секция В
@router.message(F.text == "В")
async def choose_division(message: types.Message, state: FSMContext):
        print("divb")
        strg = await state.get_data()
        dir_path1 = strg["Подотдел"]+"\\Секция В"
        undersec = "\\Секция В"
        photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
        index = 0
        strg["Savepath"] = photo[:-1]
        strg["index"] = index
        strg["Подсекция"] = undersec
        await state.update_data(strg)
        direktor = glob(photo, recursive=True)

        # В зависимости от Подразделения исполнителя, вывод фото задач, хранящихся в соответствующей директории или соответсвующего сообщения, если директория пуста
        if "Центральный" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=center_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=center_maker_kb)
        if "Барнаул" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=brn_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=brn_maker_kb)
        if "Бийск" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=bsk_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=bsk_maker_kb)
        if "Выбор" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=vybor_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=vybor_maker_kb)
        if "Майма" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=mayma_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=mayma_maker_kb)


# Если выбрана секция Д
@router.message(F.text == "Д")
async def choose_division(message: types.Message, state: FSMContext):
        print("divd")
        strg = await state.get_data()
        dir_path1 = strg["Подотдел"]+"\\Секция Д"
        undersec = "\\Секция Д"
        photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
        index = 0
        strg["Savepath"] = photo[:-1]
        strg["index"] = index
        strg["Подсекция"] = undersec
        await state.update_data(strg)
        direktor = glob(photo, recursive=True)

        # В зависимости от Подразделения исполнителя, вывод фото задач, хранящихся в соответствующей директории или соответсвующего сообщения, если директория пуста
        if "Центральный" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=center_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=center_maker_kb)
        if "Барнаул" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=brn_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=brn_maker_kb)
        if "Бийск" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=bsk_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=bsk_maker_kb)
        if "Выбор" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=vybor_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=vybor_maker_kb)
        if "Майма" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=mayma_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=mayma_maker_kb)

# Если выбрана секция М
@router.message(F.text == "М")
async def choose_division(message: types.Message, state: FSMContext):
        print("divm")
        strg = await state.get_data()
        dir_path1 = strg["Подотдел"]+"\\Секция М"
        undersec = "\\Секция М"
        photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
        index = 0
        strg["Savepath"] = photo[:-1]
        strg["index"] = index
        strg["Подсекция"] = undersec
        await state.update_data(strg)
        direktor = glob(photo, recursive=True)

        # В зависимости от Подразделения исполнителя, вывод фото задач, хранящихся в соответствующей директории или соответсвующего сообщения, если директория пуста
        if "Центральный" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=center_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=center_maker_kb)
        if "Барнаул" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=brn_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=brn_maker_kb)
        if "Бийск" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=bsk_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=bsk_maker_kb)
        if "Выбор" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=vybor_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=vybor_maker_kb)
        if "Майма" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=mayma_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=mayma_maker_kb)

# Если выбрана секция С
@router.message(F.text == "С")
async def choose_division(message: types.Message, state: FSMContext):
        print("divac")
        strg = await state.get_data()
        dir_path1 = strg["Подотдел"]+"\\Секция С"
        undersec = "\\Секция С"
        photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
        index = 0
        strg["Savepath"] = photo[:-1]
        strg["index"] = index
        strg["Подсекция"] = undersec
        await state.update_data(strg)
        direktor = glob(photo, recursive=True)

        # В зависимости от Подразделения исполнителя, вывод фото задач, хранящихся в соответствующей директории или соответсвующего сообщения, если директория пуста
        if "Центральный" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=center_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=center_maker_kb)
        if "Барнаул" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=brn_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=brn_maker_kb)
        if "Бийск" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=bsk_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=bsk_maker_kb)
        if "Выбор" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=vybor_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=vybor_maker_kb)
        if "Майма" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=mayma_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=mayma_maker_kb)

#Повторный вывод задач, хранящихся в выбранном подразделении
async def division_A(message: types.Message, state: FSMContext):
        strg = await state.get_data()
        dir_path1 = strg["Подотдел"]+"\\Секция А"
        undersec = "\\Секция А"
        photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
        index = 0
        strg["Savepath"] = photo[:-1]
        strg["index"] = index
        strg["Подсекция"] = undersec
        await state.update_data(strg)
        direktor = glob(photo, recursive=True)

        # В зависимости от Подразделения исполнителя, вывод фото задач, хранящихся в соответствующей директории или соответсвующего сообщения, если директория пуста
        if "Центральный" in strg["Подотдел"]:
            if len(direktor)==0:
                await message.answer('В этой секции задач нет', reply_markup=center_maker_kb)
            else:
                while len(direktor)!=0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=center_maker_kb)
        if "Барнаул" in strg["Подотдел"]:
            if len(direktor)==0:
                await message.answer('В этой секции задач нет', reply_markup=brn_maker_kb)
            else:
                while len(direktor)!=0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=brn_maker_kb)
        if "Бийск" in strg["Подотдел"]:
            if len(direktor)==0:
                await message.answer('В этой секции задач нет', reply_markup=bsk_maker_kb)
            else:
                while len(direktor)!=0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=bsk_maker_kb)
        if "Выбор" in strg["Подотдел"]:
            if len(direktor)==0:
                await message.answer('В этой секции задач нет', reply_markup=vybor_maker_kb)
            else:
                while len(direktor)!=0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=vybor_maker_kb)
        if "Майма" in strg["Подотдел"]:
            if len(direktor)==0:
                await message.answer('В этой секции задач нет', reply_markup=mayma_maker_kb)
            else:
                while len(direktor)!=0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document,reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=mayma_maker_kb)

#Повторный вывод задач, хранящихся в выбранном подразделении
async def division_B(message: types.Message, state: FSMContext):
        strg = await state.get_data()
        dir_path1 = strg["Подотдел"]+"\\Секция В"
        undersec = "\\Секция В"
        photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
        index = 0
        strg["Savepath"] = photo[:-1]
        strg["index"] = index
        strg["Подсекция"] = undersec
        await state.update_data(strg)
        direktor = glob(photo, recursive=True)

        # В зависимости от Подразделения исполнителя, вывод фото задач, хранящихся в соответствующей директории или соответсвующего сообщения, если директория пуста
        if "Центральный" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=center_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=center_maker_kb)
        if "Барнаул" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=brn_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=brn_maker_kb)
        if "Бийск" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=bsk_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=bsk_maker_kb)
        if "Выбор" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=vybor_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=vybor_maker_kb)
        if "Майма" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=mayma_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=mayma_maker_kb)

#Повторный вывод задач, хранящихся в выбранном подразделении
async def division_D(message: types.Message, state: FSMContext):
        strg = await state.get_data()
        dir_path1 = strg["Подотдел"]+"\\Секция Д"
        undersec = "\\Секция Д"
        photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
        index = 0
        strg["Savepath"] = photo[:-1]
        strg["index"] = index
        strg["Подсекция"] = undersec
        await state.update_data(strg)
        direktor = glob(photo, recursive=True)

        # В зависимости от Подразделения исполнителя, вывод фото задач, хранящихся в соответствующей директории или соответсвующего сообщения, если директория пуста
        if "Центральный" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=center_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=center_maker_kb)
        if "Барнаул" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=brn_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=brn_maker_kb)
        if "Бийск" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=bsk_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=bsk_maker_kb)
        if "Выбор" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=vybor_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=vybor_maker_kb)
        if "Майма" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=mayma_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=mayma_maker_kb)

#Повторный вывод задач, хранящихся в выбранном подразделении
async def division_M(message: types.Message, state: FSMContext):
        strg = await state.get_data()
        dir_path1 = strg["Подотдел"]+"\\Секция М"
        undersec = "\\Секция М"
        photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
        index = 0
        strg["Savepath"] = photo[:-1]
        strg["index"] = index
        strg["Подсекция"] = undersec
        await state.update_data(strg)
        direktor = glob(photo, recursive=True)

        # В зависимости от Подразделения исполнителя, вывод фото задач, хранящихся в соответствующей директории или соответсвующего сообщения, если директория пуста
        if "Центральный" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=center_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=center_maker_kb)
        if "Барнаул" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=brn_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=brn_maker_kb)
        if "Бийск" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=bsk_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=bsk_maker_kb)
        if "Выбор" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=vybor_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=vybor_maker_kb)
        if "Майма" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=mayma_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=mayma_maker_kb)

#Повторный вывод задач, хранящихся в выбранном подразделении
async def division_C(message: types.Message, state: FSMContext):
        strg = await state.get_data()
        dir_path1 = strg["Подотдел"]+"\\Секция С"
        undersec = "\\Секция С"
        photo = f"C:\\Users\\Admin\\PycharmProjects\\edu2023\\Telega\\start_bot\\direktory\\Фото от постановщика{dir_path1}\\*"
        index = 0
        strg["Savepath"] = photo[:-1]
        strg["index"] = index
        strg["Подсекция"] = undersec
        await state.update_data(strg)
        direktor = glob(photo, recursive=True)

        # В зависимости от Подразделения исполнителя, вывод фото задач, хранящихся в соответствующей директории или соответсвующего сообщения, если директория пуста
        if "Центральный" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=center_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=center_maker_kb)
        if "Барнаул" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=brn_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=brn_maker_kb)
        if "Бийск" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=bsk_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=bsk_maker_kb)
        if "Выбор" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=vybor_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=vybor_maker_kb)
        if "Майма" in strg["Подотдел"]:
            if len(direktor) == 0:
                await message.answer('В этой секции задач нет', reply_markup=mayma_maker_kb)
            else:
                while len(direktor) != 0:
                    document = FSInputFile(direktor[0])
                    bot = Bot("7181531660:AAHdvp0J6kPdQK237ct0ySbjcB6QSTCv2ko")
                    await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=task_kb)
                    direktor.pop(0)
                else:
                    await message.answer('Выберите задание из списка', reply_markup=mayma_maker_kb)

# если пользователь хочет выполнить поставленную задачу
@router.callback_query(F.data == "ready")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Принято. Отправьте фотоотчет")
    stringtime=await state.get_data()
    # Получение времени сохранения исправления
    msgx=callback.message
    sendtime = msgx.document.file_name[:19]
    sstime=".".join(sendtime.split("_")[:3])+" "+"-".join(sendtime.split("_")[3:6])
    stringtime["Время сохранения"] = sstime
    await state.update_data(stringtime)
    await state.set_state((States.take_photo))

#Сохранение результата выполнения задачи
@router.message(States.take_photo, F.photo)
async def ispravlenie(message: types.Message, state: FSMContext):
    path = await state.get_data()
    strtime =path["Время сохранения"]

    # Получениме даты и времени выполнения задачи, сохранение фотографии исполнения
    unix_date = message.date
    date = unix_date.strftime("%Y.%m.%d")
    time = datetime.now().strftime("%H-%M-%S")
    dest = path["Savepath"].replace("Фото от постановщика", "Фото от исполнителя")
    name = path["Fname"]
    file_ex = glob(f"{dest}")
    file_id = len(file_ex)
    undsec = path["Подсекция"]
    os.makedirs(f"{dest}", exist_ok=True)
    await message.bot.download(file=message.photo[-1], destination=f"{dest}/{date} {time}_{name}_id={file_id}.jpg")

    # запись в отчет
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
    df.to_excel("../Отчет.xlsx", index=False)

    # Удаление выполненных задач из списка поставленных задач в выбранном подразделении и секции, повторный вывод списка задач
    for el in glob(path["Savepath"]+"*"):
        if strtime in el:
            os.remove((el))
    if "А" in undsec:
        await message.answer("Отлично. Фото сохранено",reply_markup=exit_but)
        if glob(f"{dest}") != 0:

            await division_A(message, state)
        else:
            await message.answer('В этой секции задач нет',reply_markup=exit_but)
    if "В" in undsec:
        await message.answer("Отлично. Фото сохранено",reply_markup=exit_but)
        if glob(f"{dest}") != 0:

            await division_B(message, state)
        else:
            await message.answer('В этой секции задач нет',reply_markup=exit_but)
    if "Д" in undsec:
        await message.answer("Отлично. Фото сохранено",reply_markup=exit_but)
        if glob(f"{dest}") != 0:

            await division_D(message, state)
        else:
            await message.answer('В этой секции задач нет',reply_markup=exit_but)
    if "М" in undsec:
        await message.answer("Отлично. Фото сохранено",reply_markup=exit_but)
        if glob(f"{dest}") != 0:

            await division_M(message, state)
        else:
            await message.answer('В этой секции задач нет',reply_markup=exit_but)
    if "Секция С" in undsec:
        await message.answer("Отлично. Фото сохранено",reply_markup=exit_but)
        if glob(f"{dest}") != 0:

            await division_C(message, state)
        else:
            await message.answer('В этой секции задач нет',reply_markup=exit_but)

#Если нажата кнопка выход
@router.message(F.text == "Выход")
async def exit(message: types.Message, state: FSMContext):
    datas = await state.get_data()

    await message.answer("Вы постановщик или исполнитель? Нажмите (/authorization) если хотите выбрать пользователя",
                         reply_markup=role_kb)


















