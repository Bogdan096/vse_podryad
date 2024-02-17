class Person:
	def __init__(self, name):
		self.name = name
		self.age = 0
		self.status = True

	def living(self):
		self.age += 5
		if self.age >= 15:
			print(f"{self.name} прожил еще 5 лет и пошел работать на завод. Сейчас ему {self.age}, но выглядит на {self.age + 30}")
		else:
			print(f"{self.name} прожил без бед 5 лет, и ему сейчас {self.age}")






men_1 = Person("Петя")
men_2 = Person("Толя")

print(men_1.name)
men_1.living()
men_1.living()
men_1.living()


