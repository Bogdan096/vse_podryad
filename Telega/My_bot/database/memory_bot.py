import json
import os
import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext


async def load_memory(dp: Dispatcher):
    path = "memory_bot.json"
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for record in data.values():
                try:
                    await dp.storage.set_state(user=record.get("id_telegram"), state=record.get("state"))
                    await dp.storage.set_data(user=record.get("id_telegram"), data=record)
                except ValueError:
                    logging.error("Запись пропущена\n{}".format(str(record)))
                    continue
            logging.info("Хранилище данных успешно загружено")
    except FileNotFoundError:
        with open(path, "w", encoding="utf-8") as file:
            logging.error("Файла с хранилищем необнаружено, создан новый {}".format(path))
            json.dump(dict(), file)
    except json.decoder.JSONDecodeError:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(dict(), file)
            logging.error("Файла с хранилищем поврежден, создан новый {}".format(path))


async def save_memory(state: FSMContext):
    path =  "memory_bot.json"
    async with state.proxy() as data:
        try:
            with open(path, "r", encoding="utf-8") as file:
                data_from_file = json.load(file)
        except FileNotFoundError:
            with open(path, "w", encoding="utf-8") as file:
                data_from_file = dict()
                json.dump(data_from_file, file)
                logging.error("Файла с хранилищем необнаружено, создан новый {}".format(path))
        except json.decoder.JSONDecodeError:
            with open(path, "w", encoding="utf-8") as file:
                data_from_file = dict()
                json.dump(data_from_file, file)
                logging.error("Файла с хранилищем поврежден, создан новый {}".format(path))
        with open(path, "w", encoding="utf-8") as file:
            var_dict = data.as_dict()
            var_dict["state"] = data.state
            data_from_file[str(data.get("id_telegram"))] = var_dict
            json.dump(data_from_file, file, indent=2, ensure_ascii=False)


