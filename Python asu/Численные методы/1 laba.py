import time
from sys import setrecursionlimit

setrecursionlimit(1000000)
sdvig = float(0.00000001)
rng = [-2,0]
epsilon = float(0.001)
erng = [float(0.001), float(0.00001)]
min_list = []
min_func_lst = []
counter = 0

def function(x):
     return 3.7*x**4+11/(0.06+x**2)





for elem in erng:
    while abs(rng[1]-rng[0]) >= 2*elem:
        counter += 1
        x1 = (rng[0] + rng[1]) / 2 - sdvig
        x2 = (rng[0] + rng[1]) / 2 + sdvig
        y1 = function(x1)
        y2 = function(x2)
        print(f"1 функция {y1}")
        time.sleep(1)
        print(f"2 function {y2}")
        time.sleep(1)
        if y1 <= y2:
            print("меньше")
            rng = [rng[0],x2]
            time.sleep(1)
            print(rng)
        else:
            print("больше")
            rng = [x1, rng[1]]
            time.sleep(1)
            print(rng)
    minimum = (rng[1]+rng[0])/2
    min_list.append((minimum,counter))
    func_min = function(minimum)
    min_func_lst.append(func_min)
print(min_list)