"""
Условия:
    1) На основе функции полученных в 1, 2, 3 задании сделать, аналогичные действий для матрицы из
    строки состоящий из 100 чисел.

    При необходимости нужно будет скорректировать код в заданиях выполненных ранее, при этом что-бы функционал
    обеспечивал корректное выполнения каждого из заданий по отдельности. Другими словами правки не должны ломать,
    ранее выполенные задания(Файлы Матрица 1, Матрица 2, Матрица 3 должны быть точно такими же как и были,
    после выполнения задания 4

"""
# Твой код:
import task1
import task2
import task3

res_1 = task1.calling(100)


res_2 = task2.get_sum(res_1)
res_3 = task2.change_data(res_1)
res_4 = task3.get_symbols(res_1)
res_5 = task3.aggregate_it(res_4)
print(res_5)