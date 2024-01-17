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
    __validate_data_raises_ex(price_table)

    min_cost_and_path = __get_min_cost_and_path(price_table)

    return min_cost_and_path


def __get_min_cost_and_path(price_table:  list[list[float | int]]) ->\
        dict[str: float, str: list[tuple[int, int]]]:
    """Возвращает путь минимальной стоимости в таблице из правого верхнего угла
    в левый нижний.
    Каждая ячейка в таблице имеет цену посещения.
    Перемещение из ячейки в ячейку можно производить только по горизонтали
    вправо или по вертикали вниз.
    :param price_table: Таблица с ценой посещения для каждой ячейки.
    :return: Словарь с ключами:
    cost - стоимость минимального пути,
    path - путь, список кортежей с индексами ячеек.
    """

    path_table = [[INF]*(len(price_table[0]) + 1) for _ in range(len(price_table) + 1)]  # расширенный список

    for i in range(len(price_table)):  # перенос элементов в расширенный список
        for j in range(len(price_table[0])):
            path_table[i+1][j+1] = price_table[i][j]

    for i in range(1, len(path_table)):  # вычисление пути минимальной стоимости
        for j in range(1, len(path_table[0])):
            if i == j == 1:
                continue
            path_table[i][j] = path_table[i][j] + min(path_table[i-1][j], path_table[i][j-1])

    path = []

    cur_row, cur_col = len(path_table) - 1, len(path_table[0]) - 1
    while cur_row and cur_col:  # пока не дошли до начала
        path.append((cur_row-1, cur_col-1))

        if path_table[cur_row - 1][cur_col] < path_table[cur_row][cur_col - 1]:
            cur_row -= 1
        else:
            cur_col -= 1

    return {COST: path_table[-1][-1], PATH: path[::-1]}


def __validate_data_raises_ex(price_table: any):
    """Валидация таблицы и данных, содержащихся в ней.
    :param price_table: Таблица с ценой посещения для каждой ячейки.
    :raise ValueError: Если таблица цен не является прямоугольной матрицей с
    числовыми значениями.
    """

    is_error = False

    match price_table:
        case None:
            is_error = True

        case list() as lst if not len(lst):  # если список пуст
            is_error = True

        case [list() as lst] if not len(lst):  # если вложенные списки пусты
            is_error = True

        case list() as lst:   # проверка элеметов вложенных списков
            sublist_len = len(lst[0])

            for sublist in lst:  # итерация по строкам списка
                if sublist_len != len(sublist):
                    is_error = True
                    break

                for item in sublist:  # итерация по элементам строки
                    if isinstance(item, str) or item is None:
                        is_error = True
                        break
                else:  # если вложенный цикл завершился штатно, то переходим на следующую итерацию внешнего цикла
                    continue
                break

    if is_error:
        raise ValueError(PARAM_ERR_MSG)


def main():
    table = [[1, 2, 2],
             [3, 4, 2],
             [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == '__main__':
    main()
