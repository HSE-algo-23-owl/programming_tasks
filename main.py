PARAM_ERR_MSG = 'Таблица не является прямоугольной матрицей со значениями 0 1'
def get_path_count(table: list[list[int]]) -> int:
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

    validate_price_table(table)

    return number_possible_routes(table)

def validate_price_table(table):
    if table is None or table == [] or table == [[]]:
        raise ValueError(PARAM_ERR_MSG)

    rows = len(table)
    for row in table:
        if len(row) != len(table[0]):
            raise ValueError(PARAM_ERR_MSG)

        for elem in row:
            if elem not in [0, 1]:
                raise ValueError(PARAM_ERR_MSG)


def number_possible_routes (table: list[list[int]]) -> int:
    row, col = len(table), len(table[0])

    if row == 1:
        return table[0][0]

    F = [[0 for j in range(col + 1)] for i in range(row + 1)]
    # стартовый случай
    F[1][1] = table[0][0]

    for i in range(1, row + 1):
        for j in range(1, col + 1):
            if i == j == 1:
                continue
            F[i][j] = table[i - 1][j - 1] * (F[i - 1][j] + F[i][j - 1])
    return(F[-1][-1])

def main():
    table = [[1, 1, 1],
             [1, 0, 1],
             [1, 1, 1]]


if __name__ == '__main__':
    main()
