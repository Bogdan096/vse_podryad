from aiogram import types

postanova = types.InlineKeyboardButton(text = "Постановщик", callback_data="postanova")
ispolnitel = types.InlineKeyboardButton(text = "Исполнитель", callback_data="ispolnitel")
role_kb = types.InlineKeyboardMarkup(inline_keyboard=[[postanova,ispolnitel]], row_width=2)


centr = types.InlineKeyboardButton(text = "ЦБ", callback_data="Центральный офис")
vybor = types.InlineKeyboardButton(text = "Выбор", callback_data="Филиал Выбор")
brn = types.InlineKeyboardButton(text = "Барнаул", callback_data="Филиал Барнаул")
bsk = types.InlineKeyboardButton(text = "Бийск", callback_data="Филиал Бийск")
mayma = types.InlineKeyboardButton(text = "Майма", callback_data="Филиал Майма")
division_kb = types.InlineKeyboardMarkup(inline_keyboard=[[centr, vybor, brn,bsk,mayma]],row_width=5)


a = types.InlineKeyboardButton(text = "А", callback_data="Секция A")
b = types.InlineKeyboardButton(text = "В", callback_data="Секция В")
d = types.InlineKeyboardButton(text = "Д", callback_data="Секция Д")
m= types.InlineKeyboardButton(text = "М", callback_data="Секция М")
c = types.InlineKeyboardButton(text = "С", callback_data="Секция С")
brn_kb = types.InlineKeyboardMarkup(inline_keyboard=[[a, b, d, m, c]])
vybor_kb = types.InlineKeyboardMarkup(inline_keyboard=[[a, d]])
bsk_kb = types.InlineKeyboardMarkup(inline_keyboard=[[a, c]])
mayma_kb = types.InlineKeyboardMarkup(inline_keyboard=[[a, d]])
center_kb = types.InlineKeyboardMarkup(inline_keyboard=[[a, d, m, c]])


exit = types.KeyboardButton(text="Выйти")
exit_but = types.ReplyKeyboardMarkup(keyboard=[[exit]])


