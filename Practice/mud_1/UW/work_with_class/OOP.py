import random

class Person:
    def __init__(self):
        self.__hunger = 100
        self.__status = True

    @property
    def hunger(self):
        return self.__hunger

    @property
    def status(self):
        return self.__status

    def eat(self, fam:"Family"):
        fam.food_stocks -= 10
        self.__hunger += 10


    def death(self):
        self.__status = False


class Father(Person):
    def __init__(self):
        super().__init__()
        self.__role = "Кормилец"

    def __str__(self):
        return self.__role

    def __repr__(self):
        return self.__role

    def work(self, fam:"Family"):
        fam.budget += 100000
        self.__hunger -= 20

    def get_death(self):
        if self.__hunger <=0:
            self.death()
            print(f"{self.__role} погиб")

    def get_eating(self, fam: "Family"):
        if self.__hunger <= 40:
            self.eat(fam)
            print(f"{self.__role} поел")






class Mother(Person):
    def __init__(self):
        super().__init__()
        self.__role = "Домохозяйка"


    def __str__(self):
        return self.__role

    def __repr__(self):
        return self.__role


    def food_shopping(self,fam: "Family"):
        if fam.food_stocks <= 20:
            print(f"{self.__role} пошла в магазин")
            fam.food_stocks += 40
            fam.budget -= 40000
        print("Купили еду")


    def get_death(self):
        if self.__hunger <=0:
            self.death()
            print(f"{self.__role} погибла")

    def get_eating(self, fam:"Family"):
        if self.__hunger <= 40:
            self.eat(fam)
            print(f"{self.__role} поел")




class Children(Person):
    def __init__(self):
        super().__init__()
        self.__role = "Иждивенец"

    def __str__(self):
        return self.__role

    def __repr__(self):
        return self.__role

    def child_eat(self, fam:"Family"):
        self.__hunger += 20
        fam.food_stocks -= 10

    def get_death(self):
        if self.__hunger <=0:
            self.death()
            print(f"{self.__role} погиб")

    def get_сhild_eating(self, fam: "Family"):
        if self.__hunger <= 40:
            self.child_eat(fam)
            print(f"{self.__role} поел")

class Family():
    def __init__(self):
        self.__budget = random.randint(40000,250000)
        self.__house_own = "Нет"
        self.__car_own = "Нет"
        self.__food_stocks = random.randint(0,100)
        self.__person_list = []

    @property
    def budget(self):
        return self.__budget

    @budget.setter
    def budget(self, value):
        self.__budget = value

    @property
    def food_stocks(self):
        return self.__food_stocks

    @food_stocks.setter
    def food_stocks(self, value):
        self.__food_stocks = value


    def info(self):
        print(f"Состав семьи: {self.__person_list}\n Семейный бюджет: {self.__budget} рублей\n Количество еды: {self.__food_stocks}\n "
              f"Дом: {self.__house_own}\n Машина: {self.__car_own}\n\n")

    def get_buying_car(self):
        if self.__budget >= 500000:
            self.__budget -= 500000
            self.__car_own = "Есть"
            print("Семья приобрела новую машину")
        else:
            print("Недостаточно средств для приобретения")

    def get_buying_house(self):
        if self.__budget >= 2000000:
            self.__budget -= 2000000
            self.__house_own = "Есть"
            print("Семья приобрела новый дом")
        else:
            print("Недостаточно средств для приобретения")

    def add_person(self, people):
        self.__person_list.append(people)




fam = Family()
father = Father()
mother = Mother()
child = Children()
fam.add_person(father)
fam.add_person(mother)
fam.add_person(child)
fam.info()


