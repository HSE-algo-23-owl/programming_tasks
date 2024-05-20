from permutations import generate_permutations


NullableNumber = int | float | None

INFINITY = float('inf')
DISTANCE = 'distance'
PATH = 'path'
PARAM_ERR_MSG = ('Таблица расстояний не является прямоугольной матрицей с '
                 'числовыми значениями')
NEG_VALUE_ERR_MSG = 'Расстояние не может быть отрицательным'


def get_salesman_path(dist_matrix: list[list[NullableNumber]]) -> \
        dict[str, float | list[int]]:
    """Решает задачу коммивояжёра с использованием полного перебора.

    :param dist_matrix: Матрица расстояний.
    :raise TypeError: Если таблица расстояний не является прямоугольной
    матрицей с числовыми значениями.
    :raise ValueError: Если в матрице присутствует отрицательное значение.
    :return: Словарь с ключами: distance - кратчайшее расстояние,
    path - список с индексами вершин на кратчайшем маршруте.
    """
    pass


if __name__ == '__main__':
    print('Пример решения задачи коммивояжёра\n\nМатрица расстояний:')
    matrix = [[None, 12., 9., 9., 12.],
              [9., None, 8., 19., 15.],
              [7., 1., None, 17., 11.],
              [5., 9., 12., None, 16.],
              [14., 6., 12., 22., None]]
    for row in matrix:
        print(row)

    print('\nРешение задачи:')
    print(get_salesman_path(matrix))
