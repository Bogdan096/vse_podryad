
from copy import deepcopy
class Matrix(object):
    def __init__(self, matrix):
        self.matrix = deepcopy(matrix)
    def __str__(self):
        return '\n'.join('\t'.join(map(str,row)) for row in self.matrix)
    def size(self):
        return (len(self.matrix), len(self.matrix[0]))

    def __getitem__(self, idx):
        return self.matrix[idx]

    def __add__(self, other):
        if len(self.matrix) == len(other.matrix):
            lenght = len(self.matrix[0])
            result = []
            numbers = []
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    summa = other.matrix[i][j] + self.matrix[i][j]
                    numbers.append(summa)
                    if len(numbers) == len(self.matrix[0]):
                        result.append(numbers)
                        numbers = []
            return Matrix(result)
        else:
            print('')

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            result = [[other * j for j in i] for i in self.matrix]
            return Matrix(result)

    __rmul__ = __mul__

    def transpose(self):
        transMatrix = list(zip(*self.matrix))
        self.matrix = transMatrix
        return Matrix(transMatrix)

    def transposed(self):
        transMatrix = list(zip(*self.matrix))
        return Matrix(transMatrix)





