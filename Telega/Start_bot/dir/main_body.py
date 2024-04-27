
from ..handlers.parse import name_parse
from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command
from aiogram.filters import StateFilter
import datetime
import os

from Telega.start_bot.keyboards.producer_kb import (role_kb, division_kb, brn_kb,center_kb, vybor_kb, mayma_kb,
                                                    bsk_kb, exit_but, division_maker_kb, center_maker_kb)

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

@router.message(StateFilter(None), Command("authorization"))
async def cmd_auth(message: Message, state: FSMContext):
    await message.answer("Введите часть своего ФИО, а я найду его в списке")
    await state.set_state(States.fio_srch)

@router.message(States.fio_srch)
async def find_user(message:Message, state: FSMContext):
    u_message = message.text.lower()
    matches = [name for name in x if u_message in name.lower()]
    new_data= {str(index):name for index,name in enumerate(matches)}
    await state.update_data(**new_data)
    if matches:
        response_message = "\n" + "\n".join(f"{index + 1}. {name}" for index, name in enumerate(matches))
        await message.answer(response_message)
        await message.answer("Под каким ты номером?\n(введите число)")
    else:
        response_message = "Не могу найти тебя в списке :(попробуй ещё раз (/authorization) или приходи в другой раз (/stop)!"
        await message.answer(response_message)
    await state.set_state((States.choose_num))

@router.message(States.choose_num)
async def proof_user(message:Message, state: FSMContext):
    answ = message.text
    new_data = await state.get_data()
    for key,values in new_data.items():
        if answ == key:
            await message.answer(f"{new_data[str(int(key)-1)]}, вы постановщик или исполнитель?", reply_markup=role_kb)
            filename = {"Fname": f"{new_data[str(int(key)-1)]}"}
            await state.update_data(filename)

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
    os.makedirs(f"Фото от постановщика/{path['Path']}/Секция Д", exist_ok=True)
    path = {"Section": f"Фото от постановщика/{path['Path']}/Секция Д"}
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
    file_id = path["id"]
    unix_date = message.date
    date = unix_date.strftime("%Y-%m-%d")
    time = unix_date.strftime("%H_%M_%S")
    print(date)
    print(time)
    dest = path["Section"]
    name = path["Fname"]
    await message.bot.download(file=message.photo[-1], destination=f"{dest}/{date} {time}_{name}_id={file_id}).jpg")
    path[f"{dest}"].append(message.photo[-1])
    await state.update_data(path)
    await message.answer("Отлично. Фото сохранено")
    file_id += 1
    datas = {"id": file_id}
    await state.update_data(datas)


"ветка исполнителя"
@router.callback_query(F.data == "ispolnitel")
async def choose_division(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите подразделение:", reply_markup=division_maker_kb)
    await state.set_state(States.maker_stat)

@router.callback_query(F.data =='Центральный офис')
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите секцию:", reply_markup=center_maker_kb)
    div_name = {"Отдел": "Центральный офис"}
    await state.update_data(div_name)

@router.callback_query(F.data == "Филиал Выбор")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    div_name = {"Отдел": "Филиал Выбор"}
    await state.update_data(div_name)
    await callback.message.answer("Выберите секцию:", reply_markup=vybor_kb)

@router.callback_query(F.data == "Филиал Барнаул")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    div_name = {"Отдел": "Филиал Барнаул"}
    await state.update_data(div_name)
    await callback.message.answer("Выберите секцию:", reply_markup=brn_kb)

@router.callback_query(F.data == "Филиал Бийск")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    div_name = {"Отдел": "Филиал Бийск"}
    await state.update_data(div_name)
    await callback.message.answer("Выберите секцию:", reply_markup=bsk_kb)

@router.callback_query(F.data == "Филиал Майма")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    div_name = {"Отдел": "Филиал Майма"}
    await state.update_data(div_name)
    await callback.message.answer("Выберите секцию:", reply_markup= mayma_kb)

@router.callback_query(F.data == "Секция A")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = await state.get_data()
    sec_part = {"Отдел":f"{path['Отдел']}/Секция А"}
    await state.update_data(sec_part)
    await state.set_state((States.get_task))

@router.callback_query(F.data == "Секция В")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = await state.get_data()
    sec_part = {"Отдел": f"{path['Отдел']}/Секция В"}
    await state.update_data(sec_part)
    await state.set_state((States.get_task))

@router.callback_query(F.data == "Секция Д")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = await state.get_data()
    sec_part = {"Отдел": f"{path['Отдел']}/Секция Д"}
    await state.update_data(sec_part)
    await state.set_state((States.get_task))

@router.callback_query(F.data == "Секция М")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = await state.get_data()
    sec_part = {"Отдел": f"{path['Отдел']}/Секция М"}
    await state.update_data(sec_part)
    await state.set_state((States.get_task))

@router.callback_query(F.data == "Секция С")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = await state.get_data()
    sec_part = {"Отдел": f"{path['Отдел']}/Секция С"}
    await state.update_data(sec_part)
    await state.set_state((States.get_task))
























