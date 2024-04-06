from datetime import datetime, time

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

'''очистка файла перед запуском, отправка в тг по списку, запуск по расписанию, старт в 7.30'''

unames = []
spisok = []
f_spisok = []
f2_spisok = []
alive_bots = []
id_list = []
cl = []
pop_cl = []
getter_name = []
chats = tuple(id_list)


# Инициализация клиента
client = TelegramClient('test_other_variant1', 24518272, '7d643a28aaffaab9a34a04f36da6d44c',system_version="4.16.30-vxCUSTOM")

def name_parse():
    print("it works")
    path = os.path.abspath("../Боты и скрипты.xlsx")
    wb = openpyxl.load_workbook(path)
    ws = wb.sheetnames
    urls = ws[0]
    getters = ws[1]
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
    file = open("Test.txt", "a")
    user = await client.get_input_entity(username)
    await client.send_message(user, '/start')
    respond = False
    async with client.conversation(user) as conv:
        for getters in getter_name:
            getter = await client.get_entity(getters)
            try:
                response = await conv.wait_event(events.NewMessage())
                respond = True
                # await client.send_message(entity=getter, message=f"{username} активен")
                file.write(f"{username} активен\n")
                print(f"{username} активен")
            except:

                file.write(f"{username} неактивен\n")
                print(f"{username} неактивен")

    return respond



async def main():

    print('Начинаем проверку ботов...')

    await client.start()
    name_parse()

    for bot_username in id_list:
        await check_bot(bot_username)



    await client.disconnect()



with client:

    client.loop.run_until_complete(main())
#     while True:
#         if datetime.now().hour == 10:
#             print(datetime.now())
#             main()
#             print(datetime.now())
#             time.sleep(60 * 60 * 3)
#         time.sleep(60 * 15)