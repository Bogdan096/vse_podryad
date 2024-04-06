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
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def min_contact_time(mushrooms, T):
    min_time = T
    n = len(mushrooms)

    for i in range(n):
        for j in range(i + 1, n):
            distance_between_mushrooms = distance(mushrooms[i]["x"], mushrooms[i]["y"], mushrooms[j]["x"], mushrooms[j]["y"])
            contact_time = (distance_between_mushrooms - mushrooms[i]["R"] - mushrooms[j]["R"])
            if contact_time < min_time:
                min_time = contact_time

    return min_time if min_time >= 0 else 0

# Вычисляем увеличение радиуса каждого гриба после дождя
def calculate_growth(K, mushrooms, T):
    actual_growth_time = min_contact_time(mushrooms, T)
    growth_per_mushroom = [actual_growth_time * 2 for _ in range(K)]
    return growth_per_mushroom

# Функция для генерации списка грибов со случайными значениями
def generate_mushrooms(K):
    return [
        {
            "x": random.randint(0,100),  # Случайное значение для x
            "y": random.randint(0,100),  # Случайное значение для y
            "R": random.randint(1,10)   # Случайное значение для R
        } for _ in range(K)
    ]

K = 3  # Количество грибов
T = 10  # Время дождя



# Генерируем случайные данные для грибов
mushrooms = generate_mushrooms(K)

growth = calculate_growth(K, mushrooms, T)
print(growth)