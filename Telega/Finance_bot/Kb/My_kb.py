from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_kb = ReplyKeyboardMarkup(row_width=2)
start_kb.insert(KeyboardButton(text="Хочу узнать курс"))
start_kb.insert(KeyboardButton(text="Хочу конвертировать валюту"))

convert_kb = ReplyKeyboardMarkup(row_width=2)
convert_kb.insert(KeyboardButton(text="Рубль -> Доллар"))
convert_kb.insert(KeyboardButton(text="Доллар -> Рубль"))
convert_kb.insert(KeyboardButton(text="Рубль -> Евро"))
convert_kb.insert(KeyboardButton(text="Евро -> Рубль"))
convert_kb.insert(KeyboardButton(text="Рубль -> Юань"))
convert_kb.insert(KeyboardButton(text="Юань -> Рубль"))
convert_kb.insert(KeyboardButton(text="Рубль -> Тенге"))
convert_kb.insert(KeyboardButton(text="Тенге -> Рубль"))

rb = ReplyKeyboardMarkup(row_width=2)
rb.insert(KeyboardButton(text="Евро"))
rb.insert(KeyboardButton(text="Доллар"))
rb.insert(KeyboardButton(text="Тенге"))
rb.insert(KeyboardButton(text="Юань"))