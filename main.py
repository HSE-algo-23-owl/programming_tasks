PARAM_ERR_MSG = 'Таблица не является прямоугольной матрицей со значениями 0 1'


def get_path_count(allow_table: list[list[int]]) -> int:
    """Возвращает количество допустимых путей в таблице из правого верхнего угла
    в левый нижний.
    Каждая ячейка в таблице содержит 1 если ее посещение возможно и 0 если
    не возможно.
    Перемещение из ячейки в ячейку можно производить только по горизонтали
    вправо или по вертикали вниз.
    :param allow_table: Таблица с признаком возможности посещения ячеек.
    :raise ValueError: Если таблица цен не является прямоугольной матрицей
    со значениями 0 1.
    :return: количество путей.
    """
    __validate_params_raises_ex(allow_table)
    path_cnt_tbl = __get_path_cnt_tbl(allow_table)
    return path_cnt_tbl[-1][-1]


def __validate_params_raises_ex(allow_table):
    if allow_table == [] or allow_table == [[]] or allow_table == None:
        raise ValueError(PARAM_ERR_MSG)
    for row in allow_table:
        for element in row:
            if element == 1 or element == 0:
                continue
            else:
                raise ValueError(PARAM_ERR_MSG)
    if not all(len(row) == len(allow_table[0]) for row in allow_table):
        raise ValueError(PARAM_ERR_MSG)


def __get_path_cnt_tbl(allow_table):
    col_cnt = len(allow_table[0]) + 1
    row_cnt = len(allow_table) + 1
    path_cnt_tbl = [[0]*col_cnt for _ in range(row_cnt)]
    path_cnt_tbl[1][1] = allow_table[0][0]
    for row_idx in range(1, row_cnt):
        for col_idx in range(1, col_cnt):
            if row_idx == col_idx == 1:
                continue
            if allow_table[row_idx - 1][col_idx - 1] == 0:
                continue
            path_cnt_tbl[row_idx][col_idx] = (path_cnt_tbl[row_idx - 1][col_idx] + path_cnt_tbl[row_idx][col_idx - 1])
    return path_cnt_tbl


def main():
    table = [[1, 1, 1],
             [1, 0, 1],
             [1, 1, 1]]
    print(get_path_count(table))


if __name__ == '__main__':
    main()
