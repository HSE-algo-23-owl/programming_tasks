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
    # Константа сообщения об ошибке
    PARAM_ERR_MSG = "Таблица не является прямоугольной матрицей со значениями 0 1"

    # Проверка на None
    if allow_table is None:
        raise ValueError(PARAM_ERR_MSG)

    # Проверка на пустую матрицу или пустую строку
    if not allow_table or not allow_table[0]:
        raise ValueError(PARAM_ERR_MSG)

    # Проверка на некорректные значения и неравномерные строки
    row_length = len(allow_table[0])
    for row in allow_table:
        if len(row) != row_length:
            raise ValueError(PARAM_ERR_MSG)
        for value in row:
            if value not in [0, 1]:
                raise ValueError(PARAM_ERR_MSG)

    # Получение размеров матрицы
    rows, cols = len(allow_table), len(allow_table[0])

    # Проверка начальной и конечной точки
    if allow_table[0][0] == 0 or allow_table[-1][-1] == 0:
        return 0

    # Создание и инициализация матрицы путей
    paths = [[0 for _ in range(cols)] for _ in range(rows)]
    paths[0][0] = 1

    # Заполнение матрицы путей
    for i in range(rows):
        for j in range(cols):
            if allow_table[i][j] == 0:
                continue
            if i > 0:
                paths[i][j] += paths[i - 1][j]
            if j > 0:
                paths[i][j] += paths[i][j - 1]

    return paths[-1][-1]


def main():
    table = [[1, 1, 1],
             [1, 0, 1],
             [1, 1, 1]]
    print(get_path_count(table))


if __name__ == '__main__':
    main()
