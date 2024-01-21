INF = float('inf')
COST = 'cost'
PATH = 'path'
PARAM_ERR_MSG = ('Таблица цен не является прямоугольной матрицей с '
                 'числовыми значениями')


def get_min_cost_path(price_table: list[list[float | int | None]]) ->\
        dict[str: float | None, str: list[tuple[int, int]] | None]:
    """Возвращает путь минимальной стоимости в таблице из правого верхнего угла
    в левый нижний.
    Каждая ячейка в таблице имеет цену посещения.
    Некоторые ячейки запрещены к посещению, вместо цены посещения значение None.
    Перемещение из ячейки в ячейку можно производить только по горизонтали
    вправо или по вертикали вниз.
    :param price_table: Таблица с ценой посещения для каждой ячейки.
    :raise ValueError: Если таблица цен не является прямоугольной матрицей с
    числовыми значениями.
    :return: Словарь с ключами:
    cost - стоимость минимального пути или None если пути не существует,
    path - путь, список кортежей с индексами ячеек, или None если пути
    не существует.
    """
    validate_params(price_table)
    cost_table = get_cost_table(price_table)
    if cost_table[-1][-1] != INF:
        cheapest_path = find_cheapest_path(cost_table)
        return {COST: float(cost_table[-1][-1]), PATH: cheapest_path[::-1]}
    else:
        return {COST: None, PATH: None}

def validate_params(allow_table):
    if allow_table is None:
        raise ValueError("Таблица цен не является прямоугольной матрицей с числовыми значениями")
    if allow_table == []:
        raise ValueError("Таблица цен не является прямоугольной матрицей с числовыми значениями")
    for i in range(len(allow_table)):
        if allow_table[i] == []:
            raise ValueError("Таблица цен не является прямоугольной матрицей с числовыми значениями")
        if len(allow_table[0]) != len(allow_table[i]):
            raise ValueError("Таблица цен не является прямоугольной матрицей с числовыми значениями")
        for j in range(len(allow_table[i])):
            if allow_table[i][j] is None or type(allow_table[i][j]) == float or type(allow_table[i][j]) == int:
                continue
            else:
                raise ValueError("Таблица цен не является прямоугольной матрицей с числовыми значениями")



def get_cost_table(price_table):
    col_count= len(price_table[0]) + 1
    row_count= len(price_table) + 1
    cost_table= [[INF] * col_count for _ in range(row_count)]
    cost_table[1][1] = price_table[0][0]
    for row_id in range(1, row_count):
        for col_id in range(1, col_count):
            if price_table[row_id - 1][col_id - 1] is None:
                cost_table[row_id][col_id] = INF
                continue
            if row_id != 1 or col_id != 1:
                cost_up = cost_table[row_id - 1][col_id]
                cost_left = cost_table[row_id][col_id - 1]
                cost_table[row_id][col_id] = (price_table[row_id - 1][col_id - 1] + min(cost_up,cost_left))
    return cost_table

def find_cheapest_path(cost_table):

    cur_row = len(cost_table) - 1
    cur_col = len(cost_table[0]) - 1
    path_back = [(cur_row - 1, cur_col - 1)]
    while cur_row > 1 or cur_col > 1:
        cost_up = cost_table[cur_row - 1][cur_col]
        cost_left = cost_table[cur_row][cur_col - 1]
        if cost_up <= cost_left:
            cur_row -= 1
        else:
            cur_col -= 1
        path_back.append((cur_row - 1,cur_col - 1))
    return path_back

def main():
    table = [[1, 2, 2],
             [3, None, 2],
             [None, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == '__main__':
    main()
