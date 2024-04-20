
from copy import deepcopy
import numpy as np
class MatrixError(Exception):
    def __init__(self, matrix1, matrix2):
        self.matrix1 = matrix1
        self.matrix2 = matrix2

class Matrix:
    def __init__(self, list_of_lists):
        self.data = [row[:] for row in list_of_lists]  # Копирование содержимого для независимости

    def __str__(self):
        return "\n".join("\t".join(map(str, row)) for row in self.data)

    def size(self):
        return len(self.data), len(self.data[0]) if self.data else 0

    def add(self, other):
        if self.size() != other.size():
            raise MatrixError(self, other)  # Выбрасываем исключение MatrixError с передачей текущей и другой матрицы
        return Matrix([[self.data[i][j] + other.data[i][j] for j in range(len(self.data[0]))]
                       for i in range(len(self.data))])

    def mul(self, scalar):
        return Matrix([[element * scalar for element in row] for row in self.data])

    def transpose(self):
        self.data = [list(row) for row in zip(*self.data)]  # Транспонирование списка списков
        return self

    @staticmethod
    def transposed(matrix):
        return Matrix([list(row) for row in zip(*matrix.data)])  # Возвращает новую транспонированную матрицу



    # Метод rmul делающий то же, что и mul
    rmul = mul

# Использование класса Matrix и новых методов
matrix1 = Matrix([[1, 2], [3, 4]])
matrix2 = Matrix([[5, 6], [7, 8], [9, 10]])
try:
    # Разные размеры для проверки ошибки
    result_add = matrix1.add(matrix2)  # Попытка сложения матриц разного размера
except MatrixError as e:
    print("Ошибка! Матрицы разных размеров не могут быть сложены.")
    print("Матрица 1:")
    print(e.matrix1)
    print("Матрица 2:")
    print(e.matrix2)

# Транспонирование матрицы
print("Транспонирование матрицы 1:")
matrix1 = matrix1.transpose()
print(matrix1)

# Получение транспонированной матрицы через статический метод
matrix2_transposed = Matrix.transposed(matrix2)
print("Транспонированная матрица 2:")
print(matrix2_transposed)

# Использование класса Matrix
matrix1 = Matrix([[1, 2], [3, 4]])
matrix2 = Matrix([[5, 6], [7, 8]])

print(f"Матрица 1:\n{matrix1}")
print(f"Размер матрицы 1: {matrix1.size()}")

# Сложение матриц
res_add = matrix1.add(matrix2)
print(f"Сумма матриц:\n{res_add}")

# Умножение матрицы на скаляр
result_mul = matrix1.mul(10)
print(f"Матрица 1, умноженная на 10:\n{result_mul}")

# Оператор умножения, когда скаляр справа
# result_rmul = 10 * matrix1
# print(f"10 умножить на матрицу 1:\n{result_rmul}")


