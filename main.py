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

    if order == 1:
        rnd_vol = random.randint(0, 10)
        return {MATRIX: [[rnd_vol]], DET: rnd_vol}

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
    n = len(matrix)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))

    for _ in range(n):
        ind_st = random.choice([x for x in range(n)])
        ind_trg = random.choice([x for x in range(n) if x != ind_st])
        get_change_column(matrix, ind_st, ind_trg)
        ind_st = random.choice([x for x in range(n)])
        ind_trg = random.choice([x for x in range(n) if x != ind_st])
        get_change_rows(matrix, ind_st, ind_trg)

    return matrix


def get_change_column(matrix, k, m):
    for i in range(len(matrix)):
        matrix[i][k], matrix[i][m] = matrix[i][m], matrix[i][k]


def get_change_rows(matrix, k, m):
    for i in range(len(matrix)):
        matrix[k], matrix[m] = matrix[m], matrix[k]

def main():
    n = 2
    print(f"Генерация матрицы порядка {n}")
    gen_result = get_random_matrix_and_det(n)
    print('\nОпределитель сгенерированной матрицы равен', gen_result[DET])
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in gen_result[MATRIX]]))
    print('\nОпределитель, рассчитанный numpy, равен',
          round(np.linalg.det(np.array(gen_result[MATRIX]))))


if __name__ == '__main__':
    main()
