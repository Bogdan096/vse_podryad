

async def data_users_from_1c(second_name: str) -> list:
    """Функция для поиска Фамилии в справочнике пользователей и подтягиваение отдела и подр по найденому"""
    path = "//tg-storage01/Аналитический отдел/Проекты/Telegram Боты/Бот по обучению/Выгрузки/\
Сотрудники справочник (TXT).txt"
    file = open(path, "r", encoding="utf8")
    my_list_names = []
    while True:
        line = file.readline().replace("\n", "")  # считываем строку
        if not line:  # прерываем цикл, если строка пустая
            break
        line = line.split("\t")
        if second_name.lower() in line[0].split(" ")[0].lower() and line[1] == "Нет":  # поиск текста в первой части фио
            my_list_names.append([line[0], line[2], line[3]])  # фио, отдел , подразделения
    return my_list_names
