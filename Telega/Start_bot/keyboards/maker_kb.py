from aiogram import types
from .producer_kb import exit
centr = types.InlineKeyboardButton(text = "ЦБ", callback_data="ЦО")
vybor = types.InlineKeyboardButton(text = "Выбор", callback_data="Выбор")
brn = types.InlineKeyboardButton(text = "Барнаул", callback_data="Барнаул")
bsk = types.InlineKeyboardButton(text = "Бийск", callback_data="Бийск")
mayma = types.InlineKeyboardButton(text = "Майма", callback_data="Майма")
division_maker_kb = types.InlineKeyboardMarkup(inline_keyboard=[[centr, vybor, brn,bsk,mayma]],row_width=5)

#
# a = types.InlineKeyboardButton(text = "А", callback_data="A")
# b = types.InlineKeyboardButton(text = "В", callback_data="В")
# d = types.InlineKeyboardButton(text = "Д", callback_data="Д")
# m= types.InlineKeyboardButton(text = "М", callback_data="М")
# c = types.InlineKeyboardButton(text = "С", callback_data="С")
# brn_maker_kb = types.InlineKeyboardMarkup(inline_keyboard=[[a, b, d, m, c]])
# vybor_maker_kb = types.InlineKeyboardMarkup(inline_keyboard=[[a, d]])
# bsk_maker_kb = types.InlineKeyboardMarkup(inline_keyboard=[[a, c]])
# mayma_maker_kb = types.InlineKeyboardMarkup(inline_keyboard=[[a, d]])
# center_maker_kb = types.InlineKeyboardMarkup(inline_keyboard=[[a, d, m, c]])

ex = types.KeyboardButton(text = "Выход")
a = types.KeyboardButton(text = "А")
b = types.KeyboardButton(text = "В")
d = types.KeyboardButton(text = "Д")
m= types.KeyboardButton(text = "М")
c = types.KeyboardButton(text = "С")
brn_maker_kb = types.ReplyKeyboardMarkup(keyboard=[[a, b, d, m, c,ex]])
vybor_maker_kb = types.ReplyKeyboardMarkup(keyboard=[[a, d, ex]])
bsk_maker_kb = types.ReplyKeyboardMarkup(keyboard=[[a, c, ex]])
mayma_maker_kb = types.ReplyKeyboardMarkup(keyboard=[[a, d, ex]])
center_maker_kb = types.ReplyKeyboardMarkup(keyboard=[[a, d, m, c, ex]])


ready = types.InlineKeyboardButton(text="Выполнено", callback_data="ready")
next = types.InlineKeyboardButton(text="Далее", callback_data="next")

# task_kb = types.InlineKeyboardMarkup(inline_keyboard=[[next, ready, exit]])
task_kb = types.InlineKeyboardMarkup(inline_keyboard=[[ready]])

pokinut = types.KeyboardButton(text="Выход")
