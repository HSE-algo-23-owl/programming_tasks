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
    check(dist_matrix)
    n = len(dist_matrix)
    if n == 1:
        return {'distance': 0, 'path': [0]}

    vertices = frozenset(range(1, n))
    min_path = []
    min_distance = float('inf')
    generated_permutations = list(generate_permutations(vertices))
    for permutations in generated_permutations:
        current_distance = 0
        if list(permutations) is None:
            current_path = [0]
        else:
            current_path = [0] + list(permutations) + [0]
        for i in range(n):
            if dist_matrix[current_path[i]][current_path[i + 1]] is None:
                current_distance = float('inf')
                break
            else:
                current_distance += dist_matrix[current_path[i]][current_path[i + 1]]

        if current_distance < min_distance:
            min_distance = current_distance
            min_path = current_path

    if not min_path:
        return {DISTANCE: None, PATH: []}

    return {
        DISTANCE: min_distance,
        PATH: min_path
    }


def check(dist_matrix: list[list[NullableNumber]]):
    if dist_matrix is None:
        raise TypeError(PARAM_ERR_MSG)
    if not isinstance(dist_matrix, list):
        raise TypeError(PARAM_ERR_MSG)
    if len(dist_matrix) == 0:
        raise TypeError(PARAM_ERR_MSG)
    if len(dist_matrix) != len(dist_matrix[0]):
        raise TypeError(PARAM_ERR_MSG)
    first_row_len = dist_matrix[0]
    for row in dist_matrix:
        if len(row) == 0:
            raise TypeError(PARAM_ERR_MSG)
        if len(row) != len(first_row_len):
            raise TypeError(PARAM_ERR_MSG)
        if not isinstance(row, list):
            raise TypeError(PARAM_ERR_MSG)
        for elem in row:
            if not isinstance(elem, (int, float)) and elem is not None:
                raise TypeError(PARAM_ERR_MSG)
            if elem is not None:
                if elem < 0:
                    raise ValueError(NEG_VALUE_ERR_MSG)


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
