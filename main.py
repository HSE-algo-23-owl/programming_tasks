INF = float('inf')
COST = 'cost'
PATH = 'path'
PARAM_ERR_MSG = ('Таблица цен не является прямоугольной матрицей с '
                 'числовыми значениями')

def get_min_cost_path(price_table: list[list[float | int]]) ->\
        dict[str: float, str: list[tuple[int, int]]]:
    """Возвращает путь минимальной стоимости в таблице из правого верхнего угла
    в левый нижний.
    Каждая ячейка в таблице имеет цену посещения.
    Перемещение из ячейки в ячейку можно производить только по горизонтали
    вправо или по вертикали вниз.
    :param price_table: Таблица с ценой посещения для каждой ячейки.
    :raise ValueError: Если таблица цен не является прямоугольной матрицей с
    числовыми значениями.
    :return: Словарь с ключами:
    cost - стоимость минимального пути,
    path - путь, список кортежей с индексами ячеек.
    """
    validate_price_table(price_table)
    return min_cost_path(price_table)

def validate_price_table(table):
    if table is None or table == [] or table == [[]]:
        raise ValueError(PARAM_ERR_MSG)

    rows = len(table)
    for row in table:
        if len(row) != len(table[0]):
            raise ValueError(PARAM_ERR_MSG)

        for elem in row:
            if elem is None or type(elem) == str:
                raise ValueError(PARAM_ERR_MSG)

def min_cost_path (table: list[list[int]]) -> int:
    row, col = len(table), len(table[0])

    F = [[INF for j in range(col + 1)] for i in range(row + 1)]
    # стартовый случай
    F[1][1] = table[0][0]

    for i in range(1, row + 1):
        for j in range(1, col + 1):
            if i == j == 1:
                continue
            F[i][j] = (min(F[i-1][j], F[i][j-1])) + table[i-1][j-1]

    path = []
    while i != 1 or j != 1:
        path.append((i - 1, j - 1))
        if F[i][j - 1] > F[i - 1][j]:
            i -= 1
        else:
            j -= 1
    path.append((0, 0))

    return {COST: float(F[-1][-1]), PATH: path[::-1]}

def main():
    table = [[1, 2, 2],
             [3, 4, 2],
             [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == '__main__':
    main()
