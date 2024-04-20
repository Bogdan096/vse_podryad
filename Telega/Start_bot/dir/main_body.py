import asyncio
import logging

from ..handlers.parse import name_parse
from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command, CommandStart
from aiogram.filters import StateFilter
import os

from Telega.start_bot.keyboards.producer_kb import role_kb, division_kb, brn_kb,center_kb, vybor_kb, mayma_kb, bsk_kb, exit_but

router = Router()
x = name_parse()
spis = []
class States(StatesGroup):
    fio_srch = State()
    choose_num = State()
    create_task = State()

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
    else:
        response_message = "Не могу найти тебя в списке :(попробуй ещё раз (/authorization) или приходи в другой раз (/stop)!"
    await message.answer(response_message)
    await message.answer("Под каким ты номером?\n(введите число)")
    await state.set_state((States.choose_num))

@router.message(States.choose_num)
async def proof_user(message:Message, state: FSMContext):
    answ = message.text
    new_data = await state.get_data()
    for key,values in new_data.items():
        if answ == key:
            await message.answer(f"{new_data[str(int(key)-1)]}, вы постановщик или исполнитель?", reply_markup=role_kb)

@router.callback_query(F.data == "postanova")
async def choose_division(callback: types.CallbackQuery):
    os.makedirs("Фото от постановщика", exist_ok=True)
    await callback.message.answer("Выберите подразделение:", reply_markup=division_kb)

@router.callback_query(F.data =='Центральный офис')
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = {"Path": f"Фото от постановщика/Центральный офис"}
    await state.update_data(path)
    os.makedirs(f"Фото от постановщика/Центральный офис", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup=center_kb)

@router.callback_query(F.data == "Филиал Выбор")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = {"Path": f"Фото от постановщика/Филиал Выбор"}
    await state.update_data(path)
    os.makedirs(f"Фото от постановщика/Филиал Выбор", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup=vybor_kb)

@router.callback_query(F.data == "Филиал Барнаул")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = {"Path": f"Фото от постановщика/Филиал Барнаул"}
    await state.update_data(path)
    os.makedirs(f"Фото от постановщика/Филиал Барнаул", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup=brn_kb)

@router.callback_query(F.data == "Филиал Бийск")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = {"Path": f"Фото от постановщика/Филиал Бийск"}
    await state.update_data(path)
    os.makedirs(f"Фото от постановщика/Филиал Бийск", exist_ok=True)
    await callback.message.answer("Выберите секцию:", reply_markup=bsk_kb)

@router.callback_query(F.data == "Филиал Майма")
async def choose_sec1(callback: types.CallbackQuery, state: FSMContext):
    path = {"Path": f"Фото от постановщика/Филиал Майма"}
    await state.update_data(path)
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
    await state.update_data(path)
    await callback.message.answer("Прикрепите фотографию:", reply_markup=exit_but)
    await state.set_state((States.create_task))

@router.message(States.create_task)
async def create_task(message:types.Message, state: FSMContext):























