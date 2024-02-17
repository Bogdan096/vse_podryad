# класс семья, свойства колво челов(список\словарь) бюджет наличие дома и машины еда
# методы 1 узнать инфу 2 добавить члена в семью 3 исключить из семьи 4 купить дом (списать 2 млн из бюджета иначе не купить)
# 5 купить машину списать 500 тр из бюджета иначе не купить 6 пополнение 7 списание 8 купил еды 9 убарал еды (нет еды умер)
# класс член семьи, роль, сытость (0-100, <50 надо есть, сытость ноль смерть)
# метод работать (+100к, сытость -20), покупать(-50к, +40 еды), есть
# 100 дней
import random


class Family_part:
    def __init__(self, role: str, hunger: int = random.randint(30, 100)):
        self.role = role
        self.__hunger = hunger

    def work(self, family: "Family"):
        print(f"{self.role} поработал(-а)")
        family.budget += 100000
        self.hunger -= 20

    def food_shop(self, family: "Family"):
        print(f"{self.role} сходил(-а) в магазин")
        family.budget -= 50000
        family.food += 40

    def eat(self, family: "Family"):
        if family.food >= 10:
            family.food -= 10
            self.hunger += 10
        elif family.food >= 0 and family.food < 10:
            print("Мало еды. Придется идти в магазин")
            Family_part.food_shop(self, family)

    def hunger_check(self, family: "Family"):
        if self.hunger < 50:
            Family_part.eat(self, family)
    def death_event(self, family: "Family"):
        if self.hunger <= 0:
            print(f"{self.role} погиб(-ла)")


class Family:
    def __init__(self, budget:int = random.randint(40000,250000), house_own: str = "Нет", car_own: str = "Нет",
                 food: int = random.randint(0,100)):
        self.quantity = []
        self.budget = budget
        self.house_own = house_own
        self.car_own = car_own
        self.food = food

    def info(self):
        print(f"Состав семьи: {self.quantity}\n Семейный бюджет: {self.budget} рублей\n Количество еды: {self.food}\n "
              f"Дом: {self.house_own}\n Машина: {self.car_own}")


    def add_part(self, pf: "Family_part"):
        self.quantity.append(pf.role)
        print("Пополнение в семье")


    def except_part(self, pf: "Family_part"):
        self.quantity.remove(pf.role)

    def buy_house(self):
        if self.budget >= 2000000:
            self.budget -= 2000000
            self.house_own = "Есть"
            print("Семья приобрела новый дом")
        else:
            print("Недостаточно средств для приобретения")


    def buy_car(self):
        if self.budget >= 500000:
            self.budget -= 500000
            self.car_own = "Есть"
            print("Семья приобрела новую машину")
        else:
            print("Недостаточно средств для приобретения")




family = Family(food=10)
fam_part = Family_part("Отец")
family.info()
print()
family.add_part(fam_part)
family.info()
print()
fam_part.eat(family)
family.info()
fam_part.eat(family)
family.info()


