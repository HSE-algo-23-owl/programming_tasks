import numpy as np
import random


MATRIX = 'matrix'
DET = 'determinant'


def get_random_matrix_and_det(order):
    """Генерирует случайную квадратную целочисленную матрицу с заранее
    известным значением определителя.

    :param order: порядок матрицы
    :raise Exception: если порядок матрицы не является целым числом и порядок
    меньше 1
    :return: словарь с ключами matrix, det
    """
    if type(order) != int or order < 1:
        raise Exception('Error: the order is not an integer or the order less then 1!')

    determinant = 1
    # создаю пустую квадратную матрицу
    arr = []
    matrix = [[0 for j in range(order)] for i in range(order)]
    # обхожу матрицу и присваиваю рандомные значения элементам выше главной диагонали
    for i in range(order):
        for j in range(i + 1, order):
            matrix[i][j] = random.randint(1, 10)
        # Присвоение рандомного числа элементам главной диагонали
        matrix[i][i] = random.randint(1, 10)
    # Расчет детерминанта (перемножение элементов главной диагонали)
    for i in range(len(matrix)):
        determinant *= matrix[i][i]

    matrix = get_change_matrix(matrix)

    result = {MATRIX: matrix, DET: determinant}
    return result
def get_change_matrix(matrix):
    n = len(matrix) - 1
    r_st = random.randint(0, n)
    r_end = random.randint(0, n)

    # вычитание элементов строк
    for i in range(n):
        for j in range(0, len(matrix[i])):
            matrix[i][j] = matrix[i][j] - matrix[n][j]

    if r_st != r_end:
        # перемена строк и столбцоы
        for i in range(n):
            matrix[r_st], matrix[r_end] = matrix[r_end], matrix[r_st]
        for k in matrix:
            k[r_st], k[j] = k[j], k[r_st]
    else:
        for i in range(n):
            matrix[i], matrix[n - 1] = matrix[n - 1], matrix[i]

    return matrix

def main():
    n = 6
    print(f"Генерация матрицы порядка {n}")
    gen_result = get_random_matrix_and_det(n)

    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in gen_result[MATRIX]]))
    print('\nОпределитель сгенерированной матрицы равен', gen_result[DET])
    print('\nОпределитель, рассчитанный numpy, равен',
          round(np.linalg.det(np.array(gen_result[MATRIX]))))


if __name__ == '__main__':
    main()
