INF = float('inf')
COST = 'cost'
PATH = 'path'
PARAM_ERR_MSG = ('Таблица цен не является прямоугольной матрицей с '
                 'числовыми значениями')


def get_min_cost_path(price_table: list[list[float | int]]) -> \
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
    __validate_params_raises_ex(price_table)
    minimum_cost_path = __get_minimum_path_cnt_table(price_table)
    return minimum_cost_path


def __validate_params_raises_ex(price_table):
    """Проверяет являться ли таблица прямоугольной матрицей с числовыми значениями
        :param price_table: Таблица значений.
        :raise ValueError: Если таблица цен не является прямоугольной матрицей с
        числовыми значениями.
        """
    # проверяем передается ли нам таблица или нет
    if not price_table or not price_table[0]:
        raise ValueError(PARAM_ERR_MSG)
    # проверка на данные таблицы
    for row in price_table:
        for value in row:
            if not isinstance(value, (int, float)):
                raise ValueError(PARAM_ERR_MSG)
    # проверка на длину строк таблицы
    row_length = len(price_table[0])
    for row in price_table:
        if len(row) != row_length:
            raise ValueError(PARAM_ERR_MSG)


def __get_minimum_path_cnt_table(price_table: list[list[float | int]]) -> \
        dict[str: float, str: list[tuple[int, int]]]:
    """Возвращает минимальную цену и путь её нахождения
        Перемещение из ячейки в ячейку можно производить только по горизонтали
        вправо или по вертикали вниз.
        Стоимость пути из левого верхнего угла таблицы в правый нижний
        рассчитывается как сумма цен посещения всех ячеек на этом пути.
        :param price_table: Таблица с ценой посещения для каждой ячейки.
        :return: Словарь с ключами:
        min_cost - стоимость минимального пути,
        path - путь, список кортежей с индексами ячеек.
        """
    rows, cols = len(price_table), len(price_table[0])

    min_cost = [[INF] * cols for _ in range(rows)]

    min_cost[0][0] = price_table[0][0]

    for i in range(1, cols):
        min_cost[0][i] = min_cost[0][i - 1] + price_table[0][i]

    for i in range(1, rows):
        min_cost[i][0] = min_cost[i - 1][0] + price_table[i][0]

    for i in range(1, rows):
        for j in range(1, cols):
            from_above = min_cost[i - 1][j] + price_table[i][j]
            from_left = min_cost[i][j - 1] + price_table[i][j]
            min_cost[i][j] = min(from_above, from_left)

    path = [(rows - 1, cols - 1)]
    i, j = rows - 1, cols - 1
    while i > 0 or j > 0:
        if i == 0:
            path.append((i, j - 1))
            j -= 1
        elif j == 0:
            path.append((i - 1, j))
            i -= 1
        else:
            if min_cost[i - 1][j] < min_cost[i][j - 1]:
                path.append((i - 1, j))
                i -= 1
            else:
                path.append((i, j - 1))
                j -= 1

    return {
        COST: min_cost[rows - 1][cols - 1],
        PATH: list(reversed(path))}


def main():
    table = [[1, 2, 2],
             [3, 4, 2],
             [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == '__main__':
    main()
