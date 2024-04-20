from random import randint
import itertools
#1
from math import sqrt, floor

# A = int(input())
# while A > 103000:
#   print("Слишком большое число. Повторите ввод")
#   A = int(input())

# B =  floor(sqrt(A))
# print(B)

# 2
# N = int(input())
# while N < 1000 or N > 9999:
#   print("Слишком большое число. Повторите ввод")
#   N = int(input())

# thousand = N//1000
# hundred = (N % 1000) // 100
# dec = ((N % 1000) % 100) // 10
# un = N % 10
# print(thousand + hundred + dec + un, thousand*hundred*dec*un)

# 3
# s1 = str(input("Введите первую строку: "))
# s2 = str(input("Введите вторую строку: "))
#
# if sorted(s1) == sorted(s2):
#     print("Это слова анаграммы")
# else:
#     print("Это не анаграма")



#6
# sentence = str(input("Введите текст: "))
#
# words = sentence.split(' ')
# result = {}
# for word in words:
#     result[word] = result.get(word, 0) + 1
# print(result)

#7

# bundle1 = [randint(-10,10) for x in range(10)]
# bundle2= [randint(-10,10) for y in range(10)]
# nonr = []
# print(bundle1)
# print(bundle2)
# for elem1 in bundle1:
#     if not elem1 in nonr:
#         if elem1 in bundle1 and elem1 in bundle2:
#             nonr.append(elem1)
#     else:
#         continue
# print(nonr)

#8
# letters_eng = 'abcdefghijklmnopqrstuvwxyz '
# letters = dict()
#
# for pos in range(len(letters_eng)):
#     letters[letters_eng[pos]] = pos+1
#
# word = str(input("Введите строку: "))
# f_str=""
# ten_l = []
# i = 1
# for sym in word:
#   ten_l.append(int(sym, 27)-i)
#   i+=1
# for el in ten_l:
#   f_str += list(letters.keys())[el-1]
# print(f_str)
#4
import math
import random

# Функция для расчета расстояния между двумя точками
from math import sqrt


def do_mushrooms_touch(mushroom1, mushroom2):
    distance = sqrt((mushroom1['x'] - mushroom2['x'])**2 + (mushroom1['y'] - mushroom2['y'])**2)
    return distance <= (mushroom1['r'] + mushroom2['r'])

def simulate_rain(mushrooms, max_time):
    time_elapsed = 0
    while time_elapsed < max_time:
        # Увеличиваем радиусы шляпок
        for mushroom in mushrooms:
            mushroom['r'] += 1
        # Проверяем на соприкосновение
        for i in range(len(mushrooms)):
            for j in range(i + 1, len(mushrooms)):
                if do_mushrooms_touch(mushrooms[i], mushrooms[j]):
                    # Если шляпки коснулись, возвращаем результат
                    return [mushroom['r'] - mushroom['initial_r'] for mushroom in mushrooms]
        time_elapsed += 1
    # Если шляпки не соприкоснулись в течение всего дождя, возвращаем результат
    return [mushroom['r'] - mushroom['initial_r'] for mushroom in mushrooms]

# Пример использования функции:
K = 3  # количество грибов
T = 10  # время дождя в минутах
initial_mushrooms = [
    {'x': 0, 'y': 0, 'r': 2, 'initial_r': 2},  # координаты и начальный радиус 1-го гриба
    {'x': 5, 'y': 0, 'r': 2, 'initial_r': 2},  # координаты и начальный радиус 2-го гриба
    {'x': 0, 'y': 5, 'r': 2, 'initial_r': 2},  # координаты и начальный радиус 3-го гриба
]

growth = simulate_rain(initial_mushrooms, T)
print("Радиусы шляпок грибов увеличились на следующее количество сантиметров: ", growth)