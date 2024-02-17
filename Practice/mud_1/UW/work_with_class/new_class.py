class Animal:
    def __init__(self, name: str = "Животное", health: int = 10)-> None:
        self.name = name
        self.health = health
        print(f"Животное под именем {self.name} создано и имеет {self.health} здоровья")
    def battle_roar(self):
        print(f"{self.name} издает боевой клич")
        self.health += 10
        print(f"{self.name} издает боевой клич, здоровье равно {self.health}")

    def attack(self, animal: "Animal"):
        print(f"{self.name} атакует {animal.name}")
        animal.take_dmg()

    def take_dmg(self):
        self.health -= 20
        if self.health <= 0:
            print(f"{self.name} умер")
        else:
            print(f"{self.name} имеет {self.health} здоровья")

my_an = Animal("Бобик", 100)
my_an2 = Animal("Тузик", 57)
my_an.battle_roar()
my_an2.attack(my_an)
my_an2.attack(my_an)
my_an.attack(my_an2)
my_an.attack(my_an2)
my_an.attack(my_an2)

