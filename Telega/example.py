
async def query_handle(query: types.CallbackQuery, state: FSMContext):
    """После нажатия кнопку должна выпасть позиция для проверки"""
    pass



kb = types.InlineKeyboardMarkup(row_width=1)
kb.insert(types.InlineKeyboardButton(text="Не удалось найти", callback_data="check_no_{}_{}".
                                     format(id_pos, id_user),))


dp.register_callback_query_handler(query_handle,
                                    lambda callback_query: callback_query.data.startswith("check_"),
                                    state="*")

