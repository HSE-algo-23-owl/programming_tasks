import random

import numpy as np
import random as rnd


MATRIX = 'matrix'
DET = 'det'


def get_random_matrix_and_det(order):
    """Генерирует случайную квадратную целочисленную матрицу с заранее
    известным значением определителя.

    :param order: порядок матрицы
    :raise Exception: если порядок матрицы не является целым числом и порядок
    меньше 1
    :return: словарь с ключами matrix, det
    """
    if type(order)!= int :
        raise Exception('Порядок матрицы не является целым числом')
    elif order<1:
        raise Exception('Порядок матрицы меньше 1')
    matrix =[]
    for i in range (order):
        matrix.append([0]*order)
    det = 1
    i = 0
    for a in range(order):
        for b in range(i, order):
            matrix[a][b] = (rnd.randint(1, 10))
        det *= matrix[a][i]
        i = i + 1
    result ={MATRIX: matrix, DET: det}
    return result

def main():
    n = 10
    print('Генерация матрицы порядка 10')
    gen_result = get_random_matrix_and_det(n)
    [print(row) for row in gen_result[MATRIX]]
    print('\nОпределитель сгенерированной матрицы равен', gen_result[DET])

    print('\nОпределитель, рассчитанный numpy, равен',
          round(np.linalg.det(np.array(gen_result[MATRIX]))))


if __name__ == '__main__':
    main()
