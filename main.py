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
    pass


def main():
    table = [[1, 1, 1],
             [1, 0, 1],
             [1, 1, 1]]
    print(get_path_count(table))


if __name__ == '__main__':
    main()
