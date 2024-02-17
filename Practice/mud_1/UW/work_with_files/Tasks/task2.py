"""
Условия:
    1) Вывести на экран данные полученные из файла с первой задачи(написать функцию для этого).

    2) Создать функцию get_sum, которая должна принимать на вход значение с данными из файла первой задачи.
    А возвращать сумму всех полученных чисел.

    3) Создать функцию change_data, которая должна принимать на вход значение с данными из файла первой задачи.
    Посчитать сумму по каждой строке и каждому столбцу, и добавить их к исходным данным в n+1 строку
    и в n+1 столбец соответственно(Общий итог так же должен быть(пересечение итогов суммы и столбцов,
    должно быть заполенно)
    Измененные данные должны быть возвращены этой функцией.

    4) Результат функции change_data сохранить в отдельный файл "Матрица 2.txt"

    Сопроводить все действия логирование.(делать print с информативными данными о том,
    что происходит во время выполнения кода)

"""
# Твой код:
def read_f(path: str) -> str:
    """"Эта функция возвращает текст из файла"""
    with open(path, 'r', encoding = "utf-8") as file:
        otvet = file.read()
        return otvet

def get_sum(doc: str) -> int:
    x = doc.split()

    x = [int(elem) for elem in x]
    return sum(x)


def change_data(doc: str) -> str:
    spisok = []
    for elem in doc.split("\n"):
        s = 0
        x = elem.split()
        for data in x:
            s = int(s)
            s += int(data)
            s = str(s)
        x.append(s)
        spisok.append(x)

    listing = [0 for _ in range(len(spisok) + 1)]

    for i in range(len(listing)):
        for j in spisok:
            listing[i] = int(listing[i])
            listing[i] += int(j[i])
            listing[i] = str(listing[i])
    spisok.append(listing)
    peremennaya = ''
    for f in range(len(spisok)):
        peremennaya += ' '.join(spisok[f]) + '\n'
    return peremennaya

def save_data(func_res: str) -> None:
    with open("Матрица_2.txt", "w", encoding="utf-8") as file:
        file.write(func_res[:-1])


if __name__ == "__main__":
    gotoviy_f = read_f("Матрица.txt")
    re_text = change_data(gotoviy_f)
    save_data(re_text)

