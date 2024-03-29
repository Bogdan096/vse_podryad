# Запись/чтение кортежа, содержащего разнотипные объекты
# 1. Запись кортежа в файл

# 1.1. Исходный кортеж
T1 = ( 5, True, "abcde fghi")

# 1.2. Открыть файл для записи в текстовом режиме
f = open('myfile4.txt', 'wt')

# 1.3. Поэлементная запись кортежа в файл,
# поскольку в кортеже есть строки, то записываем
# каждый элемент в отдельную строку
for item in T1:
    s = str(item) + '\n' # добавить символ новой строки
    f.write(s)

# Закрыть файл
f.close()

# 2. Чтение кортежа
f = open('myfile4.txt', 'rt')

# 2.1. Создать пустой кортеж
T3 = ()

# 2.2. Чтение данных из файла и создание кортежа
# Первым читается число типа int
s = f.readline()
T3 = T3 + (int(s),) # конкатенация кортежей

# Вторым читается логическое значение типа bool
s = f.readline()
T3 = T3 + (bool(s),)

# Третьим читается строка типа str
s = f.readline()
s = s.rstrip() # убрать символ '\n' из строки
T3 = T3 + (s,)

# 2.3. Вывести кортеж для контроля
print("T3 = ", T3) # T3 = (5, True, 'abcde fghi')

# 2.4. Закрыть файл
f.close()