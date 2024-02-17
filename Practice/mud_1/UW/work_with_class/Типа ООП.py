

# class Dog:
# 	"""Инкапсуляция"""
# 	def __init__(self, name):
# 		self.__name = name
# 		self.__age = 0
#
# 	def get_name(self):
# 		print(f"Собаку зовут {self.__name}")
# 		return self.__name
#
# 	def get_age(self):
# 		print(f"Собаке {self.__age} лет")
# 		return self.__age
#
# 	def set_age(self, value: int):
# 		self.__age = value
#
#
# dog = Dog("жучка")
# dog.get_name()
# dog.get_age()
# dog.set_age(10)
# dog.get_age()

# class Dog:
# 	"""Инкапсуляция"""
# 	def __init__(self, name):
# 		self.__name = name
# 		self.__age = 0
# 		self.__status = []
#
# 	@property
# 	def name(self):
# 		"""Это метод для получения имени экземпляра класса"""
# 		return self.__name
#
# 	@name.setter
# 	def name(self, value: int):
# 		self.__name = value
#
# 	def some_method(self):
# 		self.__status = True
#
# 	def other_method(self):
# 		if self.__status:
# 			return  2
#
# dog = Dog("жучка")
# print(dog.name)
# dog.name = "Не жуччка"
# print(dog.name)


#
# import time
#
#
# def timer(func):
# 	def wrapped_func(*args, **kwargs):
# 		t1 = time.time()
# 		result = func(*args, **kwargs)
# 		t2 = time.time()
# 		print("Время выполнения код =", t2 - t1)
# 		return result
#
# 	return wrapped_func
#
#
# @timer
# def our_func():
# 	print(3)
#
#
# @timer
# def our_func2():
# 	print(3)
#
#
# our_func()
# print()
# our_func()
# our_func2()


class Animal:

	def __init__(self):
		self.__health = 100

	@property
	def health(self):
		return self.__health

	@health.setter
	def health(self, value: int):
		self.__health = value

	def voice(self):
		print("Издаёт звук")


class Cat(Animal):

	def __init__(self):
		super().__init__()

	def voice(self):
		print("Мяу")


class Dog(Animal):

	def __init__(self):
		super().__init__()

	def voice(self):
		print("Гав")



my_cat = Cat()
my_dog = Dog()
my_cat.voice()
my_dog.voice()


