from __future__ import annotations

import sys
max_int = sys.maxsize
COST = 'cost'
PATH = 'path'
PARAM_ERR_MSG = ('Таблица цен не является прямоугольной матрицей с '
                 'числовыми значениями')


def __validate_matrix(matrix):
    if matrix == None or len(matrix) <= 0 or len(matrix[0]) <=0:
        raise ValueError(PARAM_ERR_MSG)
    a=set()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if isinstance(matrix[i][j], str):
                raise ValueError(PARAM_ERR_MSG)
        a.add(len(matrix[i]))
    if len(a) > 1:
        raise ValueError(PARAM_ERR_MSG)


def get_min_cost_path(matrix: list[list[float | int | None]]) ->\
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
    __validate_matrix(matrix)
    m, n = len(matrix), len(matrix[0])
    path_matrix = [[0 for _ in range(n)] for _ in range(m)]
    if matrix[0][0] == None:
        dict1 = {COST: None, PATH: None}
        return dict1
    else:
        path_matrix[0][0] = matrix[0][0]
    for i in range(1, n):
        if matrix[0][i] is None:
            path_matrix[0][i] = max_int
        else:
            path_matrix[0][i] = path_matrix[0][i - 1] + matrix[0][i]
    for j in range(1, m):
        if matrix[j][0] is None:
            path_matrix[j][0] = max_int
        else:
            path_matrix[j][0] = path_matrix[j - 1][0] + matrix[j][0]
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] is None:
                matrix[i][j] = max_int
            path_matrix[i][j] = min(path_matrix[i - 1][j], path_matrix[i][j - 1]) + matrix[i][j]
    flag = True
    row= m - 1
    colummn = n - 1
    a = [(row, colummn)]
    while not (row == 0 and colummn == 0):
        if path_matrix[row][colummn - 1] < path_matrix[row - 1][colummn]:
            colummn -= 1
            a.append((row, colummn))
        else:
            row -= 1
            a.append((row, colummn))
        if row == 0 and colummn != 0:
            colummn -= 1
            a.append((row, colummn))
        if row != 0 and colummn == 0:
            row -= 1
            a.append((row, colummn))
    a.reverse()
    if path_matrix[-1][-1] >= max_int:
        dict1 = {COST: None, PATH: None}
    else:
        dict1 = {COST: path_matrix[-1][-1], PATH: a}
    return dict1


def main():
    table = [[None]]
    print(get_min_cost_path(table))


if __name__ == '__main__':
    main()
