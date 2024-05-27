from permutations import generate_permutations

NullableNumber = int | float | None

INFINITY = float('inf')
DISTANCE = 'distance'
PATH = 'path'
PARAM_ERR_MSG = ('Таблица расстояний не является прямоугольной матрицей с '
                 'числовыми значениями')
NEG_VALUE_ERR_MSG = 'Расстояние не может быть отрицательным'
MAX_VERTEXES = 15
MAX_VERTEXES_ERR_MSG = f'Количество вершин не может быть больше чем {MAX_VERTEXES}'



def get_salesman_path(dist_matrix: list[list[NullableNumber]]) -> \
        dict[str, float | list[int]]:
    if not isinstance(dist_matrix, list) or not dist_matrix:
        raise TypeError(PARAM_ERR_MSG)

    if not all(isinstance(row, list) for row in dist_matrix):
        raise TypeError(PARAM_ERR_MSG)
    num_vertexes = len(dist_matrix)
    if not all(len(row) == num_vertexes for row in dist_matrix):
        raise TypeError(PARAM_ERR_MSG)
    for row in dist_matrix:
        for cell in row:
            if not (isinstance(cell, (int, float)) or cell is None):
                raise TypeError(PARAM_ERR_MSG)
            if isinstance(cell, (int, float)) and cell < 0:
                raise ValueError(NEG_VALUE_ERR_MSG)
    if num_vertexes > MAX_VERTEXES:
        raise ValueError(MAX_VERTEXES_ERR_MSG)

    if num_vertexes == 1:
        return {DISTANCE: 0, PATH: [0]}


    vertices = frozenset(range(1, num_vertexes))
    min_distance = INFINITY
    best_path = []
    permutations = generate_permutations(vertices)

    for permutation in permutations:
        permutation = [0] + permutation
        current_distance = 0
        is_valid_path = True
        for i in range(num_vertexes - 1):
            if dist_matrix[permutation[i]][permutation[i + 1]] is None:
                is_valid_path = False
                break
            current_distance += dist_matrix[permutation[i]][permutation[i + 1]]
        if is_valid_path and dist_matrix[permutation[-1]][permutation[0]] is not None:
            current_distance += dist_matrix[permutation[-1]][permutation[0]]
            if current_distance < min_distance:
                min_distance = current_distance
                best_path = permutation
    if min_distance == INFINITY:
        return {DISTANCE: None, PATH: []}

    return {
        DISTANCE: min_distance,
        PATH: best_path + [best_path[0]]
    }

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