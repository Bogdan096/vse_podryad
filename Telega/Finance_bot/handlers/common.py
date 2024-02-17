from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from Kb.My_kb import start_kb, rb, convert_kb


import datetime
import logging
import requests
from bs4 import BeautifulSoup

slovar = {}
async def values(dictionary: dict):
    url = "https://finance.rambler.ru/currencies/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    ten_val = soup.find("a", title="Казахских тенге")
    dol_val = soup.find("a", title="Доллар США")
    eur_val = soup.find("a", title="Евро")
    ju_val = soup.find("a", title="Китайских юаней")
    tenge_val = ten_val.find("div",
                             class_="finance-currency-table__cell finance-currency-table__cell--value").text.strip()
    dollar_val = dol_val.find("div",
                             class_="finance-currency-table__cell finance-currency-table__cell--value").text.strip()
    euro_val = eur_val.find("div",
                             class_="finance-currency-table__cell finance-currency-table__cell--value").text.strip()
    juang_val = ju_val.find("div",
                             class_="finance-currency-table__cell finance-currency-table__cell--value").text.strip()

    dictionary["Тенге"] = round(float(tenge_val)/100, 4)
    dictionary["Доллар"] = float(dollar_val)
    dictionary["Евро"] = float(euro_val)
    dictionary["Юань"] = float(juang_val) / 10



class FSMCommon(StatesGroup):
    chose_state = State()
    get_val_state = State()
    convert_state = State()
    rub_change_state = State()
    other_change_state = State()


async def cmd_start(message: types.Message, state: FSMContext):
    await values(slovar)
    await message.answer("Привет! Я бот-валютчик.\n Я умею парсить курсы валют. Выберите действие:")

    await message.answer("Выберите действие:",reply_markup=start_kb)
    await FSMCommon.chose_state.set()

async def chose_func(message: types.Message, state: FSMContext):
    if message.text == "Хочу узнать курс":

        await message.answer("Выберите нужную валюту", reply_markup=rb)
        await FSMCommon.get_val_state.set()
    elif message.text == "Хочу конвертировать валюту":

        await message.answer("Выберите способ конвертации", reply_markup=convert_kb)
        await FSMCommon.convert_state.set()
async def get_val(message: types.Message, state: FSMContext):
    await values(slovar)
    dt = datetime.date.today()
    if message.text in ["Евро", "Доллар", "Юань", "Тенге"]:
        await message.answer(f"На {dt} курс {message.text.lower()} = {slovar[message.text]} рублей")
        await message.answer("Выберите действие", reply_markup=start_kb)
        await FSMCommon.chose_state.set()


async def convert_val(message: types.Message, state: FSMContext):
    await values(slovar)
    async with state.proxy() as dataset:
        for key in slovar.keys():
            if message.text == f"Рубль -> {key}":
                dataset["Выбранная валюта"] = key
                await message.answer("Введите желаемую сумму для конвертации")
                await FSMCommon.rub_change_state.set()
            elif message.text == f"{key} -> Рубль":
                dataset["Выбранная валюта"] = key
                await message.answer("Введите желаемую сумму для конвертации")
                await FSMCommon.other_change_state.set()

async def rub_change(message: types.Message, state: FSMContext):
    async with state.proxy() as dataset:
        summa = float(message.text)
        await message.answer(f'{summa} рублей = {round(summa/slovar[dataset["Выбранная валюта"]], 3)} '
                         f'{dataset["Выбранная валюта"]}')

        await message.answer("Выберите действие:", reply_markup=start_kb)
        await FSMCommon.chose_state.set()

async def other_change(message: types.Message, state: FSMContext):
    async with state.proxy() as dataset:
        summa = int(message.text)
        await message.answer(f'{summa} {dataset["Выбранная валюта"]} ='
                             f' {round(summa*slovar[dataset["Выбранная валюта"]], 3)} рублей')

        await message.answer("Выберите действие:", reply_markup=start_kb)
        await FSMCommon.chose_state.set()
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands = "start", state="*")
    dp.register_message_handler(chose_func, state=FSMCommon.chose_state)
    dp.register_message_handler(get_val, state=FSMCommon.get_val_state)
    dp.register_message_handler(convert_val, state=FSMCommon.convert_state)
    dp.register_message_handler(rub_change, state=FSMCommon.rub_change_state)
    dp.register_message_handler(other_change, state=FSMCommon.other_change_state)








