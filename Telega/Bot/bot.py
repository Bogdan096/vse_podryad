from aiogram.utils import executor
from aiogram.types import BotCommand
import asyncio
import os
from datetime import datetime
import json
import pandas as pd


import logging

from create_bot import dp
from handlers import common, studies, observation
from database import memory_bot

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    logging.info("Бот по обучению онлайн")
    await memory_bot.load_memory(dp)
    commands = [
        BotCommand(command="/authorization", description="Авторизация"),
        BotCommand(command="/actions", description="Доступные действия"),
        BotCommand(command="/about_me", description="Информация о пользователе"),
    ]
    await dp.bot.set_my_commands(commands)
    asyncio.create_task(save_to_excel())


async def save_to_excel():
    while True:
        path = os.sep * 2 + os.path.join("tg-storage01", "Аналитический отдел", "Проекты", "Telegram Боты",
                                         "Бот по обучению V2", "Выгрузки", "Наблюдение")
        path_to_file =\
            os.path.join(path, "Данные об обучении {}.json".format(datetime.now().replace(day=1).strftime("%d.%m.%Y")))
        path_to_file_excl = path_to_file.replace(".json", ".xlsx").replace("Наблюдение", "Наблюдение(xlsx)")
        if os.path.exists(path_to_file):
            with open(path_to_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            df = pd.DataFrame()
            df["Кто"] = ""
            df["Филиал Кто"] = ""
            df["Отдел кто"] = ""
            df["Кого"] = ""
            df["Отдел Кого"] = ""
            df["Филиал Кого"] = ""
            df["Время начала"] = ""
            df["Время конца"] = ""
            df["Длительность"] = ""
            df["Запрос клиента"] = ""
            df["Номер вопроса"] = ""
            df["Точки роста"] = ""
            df["Блок"] = ""
            df["Категория"] = ""
            df["Заработанные баллы"] = ""
            for elem in data:
                len_qw = 0
                for key, value in elem.get("Current proc").get("Check list").items():
                    len_qw += len(value)
                for key, value in elem.get("Current proc").get("Check list").items():
                    for key2, value2 in value.items():
                        cat_list = key2.split(";")
                        list_to_row = list()
                        list_to_row.append(elem.get("User"))
                        list_to_row.append(elem.get("User_filial"))
                        list_to_row.append(elem.get("User_otdel"))
                        list_to_row.append(elem.get("Current proc").get("Users").get("User"))
                        list_to_row.append(elem.get("Current proc").get("Users").get("User_filial"))
                        list_to_row.append(elem.get("Current proc").get("Users").get("User_otdel"))
                        list_to_row.append(elem.get("Current proc").get("Time start"))
                        list_to_row.append(elem.get("Current proc").get("Time finish"))
                        list_to_row.append(round(elem.get("Current proc").get("Duration") / len_qw, 2))
                        list_to_row.append(elem.get("Current proc").get("query client"))
                        list_to_row.append(cat_list[0])
                        list_to_row.append(elem.get("Current proc").get("point up"))
                        list_to_row.append(key)
                        list_to_row.append(cat_list[1])
                        list_to_row.append(value2)
                        df.loc[len(df)] = list_to_row
            try:
                with pd.ExcelWriter(path_to_file_excl) as writer:
                    df.to_excel(writer, sheet_name="Данные", index=False)
            except PermissionError:
                continue
        await asyncio.sleep(60 * 10)


common.register_handlers(dp)
studies.register_handlers(dp)
observation.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
