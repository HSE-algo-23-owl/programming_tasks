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
    checkIfMatrixIsValid(allow_table)
    rows = len(allow_table)
    cols = len(allow_table[0])
    # Создаем матрицу для хранения кол-ва путей
    paths = [[0] * cols for i in range(rows)]
    paths[0][0] = 1
    # заполняем первую строку
    for col in range(1, cols):
        if allow_table[0][col] == 1:
            paths[0][col] = paths[0][col - 1]
    # заполняем первый столбец
    for row in range(1, rows):
        if allow_table[row][0] == 1:
            paths[row][0] = paths[row-1][0]
    # заполняем остальные ячейки
    for row in range(1,rows):
        for col in range(1,cols):
            if allow_table[row][col] == 1:
                paths[row][col] = paths [row - 1][col] + paths [row][col-1]
    # возваращаем 0, если у начальной матрицы одна ячейка с нулем
    if rows == 1 and cols == 1 and allow_table[0][0] == 0:
        return 0
    return paths[-1][-1]

def checkIfMatrixIsValid( matrix: list[list[int]]):
    # Проверка на верность переданных данных
    if matrix is None:
        raise ValueError(PARAM_ERR_MSG)
    if not matrix or not matrix[0]:
        raise ValueError(PARAM_ERR_MSG)
    cols = len(matrix[0])
    for row in matrix:
        if len(row) != cols or not all(val in (0,1) for val in row) or matrix == None:
            raise ValueError(PARAM_ERR_MSG)

def main():
    table = [[1, 1, 1],
             [1, 0, 1],
             [1, 1, 1]]
    print(get_path_count(table))


if __name__ == '__main__':
    main()
 
