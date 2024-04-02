import requests
from bs4 import BeautifulSoup
import asyncio
import itertools
import logging
import pandas as pd
from aiogram.handlers import message
from entrance_data import api_id, api_hash
from telethon import TelegramClient, events
import os
import openpyxl




unames = []
spisok = []
alive_bots = []
id_list = ["Start_Checker_bot", "Bodyapkin_bot" ]
cl = []
pop_cl = []
getter_name = ["shwedskii_navodchik"]
chats = tuple(id_list)
flag = 0
bots_to_check = ['Start_Checker_bot', 'Bodyapkin_bot']

# Инициализация клиента
client = TelegramClient('test_other_variant', api_id, api_hash,system_version="4.16.30-vxCUSTOM")

def name_parse():
    print("it works")
    path = os.path.abspath("../Боты и скрипты.xlsx")
    wb = openpyxl.load_workbook(path)
    ws = wb.sheetnames
    urls = ws[0]
    getters = ws[1]
    print("it workz")
    for i in range(0, wb[urls].max_row):
        for col in wb[urls].iter_cols(1, 3):
            if "https" in str(col[i].value):
                spisok.append(str(col[i].value))
    for i in range(1, wb[getters].max_row):
        for col in wb[getters].iter_cols(2):
            getter_name.append(str(col[i].value))
    for link in spisok:
        resp = requests.get(link)
        soup = BeautifulSoup(resp.text, "lxml")
        name = soup.find(class_="tgme_page_title")
        username = soup.find(class_="tgme_page_extra")

        id_list.append(username.text[4:])

async def check_bot(username: str):
    user = await client.get_input_entity(username)
    await client.send_message(user, '/start')
    respond = False
    async with client.conversation(user) as conv:
        for getters in getter_name:
            getter = await client.get_entity(getters)
            try:
                response = await conv.wait_event(events.NewMessage())
                respond = True
                await client.send_message(entity=getter, message=f"{username} активен")
            except:
                await client.send_message(entity=getter, message=f"{username} неактивен")
        return respond

async def main():
    print('Начинаем проверку ботов...')
    # Авторизуемся и запускаем клиент
    await client.start()
    # name_parse()
    # Проверяем каждого бота
    for bot_username in id_list:
        await check_bot(bot_username)

    # Отключаемся от Telegram
    await client.disconnect()

# Запускаем программу
with client:
    client.loop.run_until_complete(main())