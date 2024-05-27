from permutations import generate_permutations

NullableNumber = int | float | None

INFINITY = float('inf')
DISTANCE = 'distance'
PATH = 'path'
PARAM_ERR_MSG = ('Таблица расстояний не является прямоугольной матрицей с '
                 'числовыми значениями')
NEG_VALUE_ERR_MSG = 'Расстояние не может быть отрицательным'
MAX_VERTICES = 10


def validate_matrix(matrix: list[list[NullableNumber]]) -> None:
    """Проверяет корректность входной матрицы."""
    if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise TypeError(PARAM_ERR_MSG)

    rows = len(matrix)
    if rows == 0:
        raise TypeError(PARAM_ERR_MSG)

    for row in matrix:
        if len(row) != rows:
            raise TypeError(PARAM_ERR_MSG)
        for value in row:
            if not isinstance(value, (int, float, type(None))):
                raise TypeError(PARAM_ERR_MSG)
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError(NEG_VALUE_ERR_MSG)


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
    validate_matrix(dist_matrix)

    n = len(dist_matrix)
    if n > MAX_VERTICES:
        raise ValueError(f'Количество вершин в графе не может превышать {MAX_VERTICES}')

    if n == 1:
        return {DISTANCE: 0, PATH: [0]}

    def calculate_path_length(path):
        length = 0
        for i in range(len(path) - 1):
            if dist_matrix[path[i]][path[i + 1]] is None:
                return INFINITY
            length += dist_matrix[path[i]][path[i + 1]]
        return length

    vertices = list(range(n))
    min_path = None
    min_distance = INFINITY

    for perm in generate_permutations(frozenset(vertices[1:])):
        path = [vertices[0]] + list(perm) + [vertices[0]]
        current_distance = calculate_path_length(path)
        if current_distance < min_distance:
            min_distance = current_distance
            min_path = path

    if min_distance == INFINITY:
        return {DISTANCE: None, PATH: []}

    return {DISTANCE: min_distance, PATH: min_path}


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
