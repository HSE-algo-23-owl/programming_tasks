import numpy as np
import random as rnd

MATRIX = 'matrix'
DET = 'det'


def input_exception(order: int):
    if type(order) != int:
        raise Exception('Порядок матрицы не является целым числом')
    if order < 1:
        raise Exception('Порядок матрицы меньше 1')


def get_matrix(order: int) -> [[int]]:  # генерация матрици с определителем = 1
    matrix = []
    for i in range(order):
        matrix.append([1] * order)
    for i in range(order - 1):
        matrix[i][i] += 1
    return matrix


def get_random_matrix_and_det(order: int):
    input_exception(order)
    det = 1
    matrix = get_matrix(order)
    for i in range(order):
        rand1 = rnd.randint(1, 10)  # можно поменять значения; чем больше значение, тем более разные числа
        rand2 = rnd.randint(1, 10)
        for j in range(order):
            matrix[i][j] *= rand1
            matrix[j][i] *= rand2
        det *= rand2 * rand1

    matrix_and_det = {MATRIX: matrix, DET: det}
    return matrix_and_det


def main():
    n = 10.1
    print('Генерация матрицы порядка 10')
    gen_result = get_random_matrix_and_det(n)
    [print(row) for row in gen_result[MATRIX]]
    print('\nОпределитель сгенерированной матрицы равен', gen_result[DET])

    print('\nОпределитель, рассчитанный numpy, равен',
          round(np.linalg.det(np.array(gen_result[MATRIX]))))


if __name__ == '__main__':
    main()
