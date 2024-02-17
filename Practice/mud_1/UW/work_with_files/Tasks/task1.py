"""
Условия:
    1) Написать функцию get_rows_with_ten_numbers,
    в ход стоит необязательный аргумент, с числом необходимых значений, по умолчанию = 10.
     которая будет возвращать n произвольных чисел от 65 до 90 или от 48 до 57 записанных в одну строку с табуляцией(\t)
     в качестве разделителя.

    2) Создать файл "Матрица.txt", которая будет состоять из n различных строк(количество строк равно количеству чисел),
     полученных с помощью get_rows_with_ten_numbers
        Нужно сделать два варианты исполнения этого пункта:
            - Все данные должны быть записаны в файл единоразово.
            - Все данные файл должны быть записаны по мере поступления.
        Ничего кроме чисел, табуляций и переносов каретки в файле быть не должно


    Сопроводить все действия логирование.(делать print с информативными данными о том,
    какой процесс сейчас происходит)
"""
# Твой код:
from typing import List
from random import randint
def get_rows_with_ten_numbers(count: int = 10) -> str:
    """"Функция для генераций списка случайных значений"""
    result_list = list()

    for num in range(count):
        if randint(0, 1):
            result_list.append(str(randint(65, 90)))
        else:
            result_list.append(str(randint(48, 57)))
    stroka = '\t'.join(result_list)
    return stroka



def save_result(val: str):
    with open("Матрица.txt", 'w', encoding = 'utf-8') as file:
        file.write(val[:-1])



print("Запускается процедура")
res = ''
for _ in range(10):
    print(_/10, "выполнено")
    v = get_rows_with_ten_numbers()
    res += v + '\n'
print("Сохраняем файл")
save_result(res)
print("Файл сохранен")



