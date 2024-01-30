from copy import deepcopy

import numpy as np

PROFIT = 'profit'
DISTRIBUTION = 'distribution'
PARAM_ERR_MSG = ('Таблица прибыли от проектов не является прямоугольной '
                 'матрицей с числовыми значениями')
NEG_PROFIT_ERR_MSG = 'Значение прибыли не может быть отрицательно'
DECR_PROFIT_ERR_MSG = 'Значение прибыли не может убывать с ростом инвестиций'


class ProfitValueError(Exception):
    def __init__(self, message, project_idx, row_idx):
        self.project_idx = project_idx
        self.row_idx = row_idx
        super().__init__(message)


def get_invest_distribution(profit_matrix: list[list[int]]) -> \
        dict[str: int, str: list[int]]:
    """Рассчитывает максимально возможную прибыль и распределение инвестиций
    между несколькими проектами. Инвестиции распределяются кратными частями.
    :param profit_matrix: Таблица с распределением прибыли от проектов в
    зависимости от уровня инвестиций. Проекты указаны в столбцах, уровни
    инвестиций в строках.
    :raise ValueError: Если таблица прибыли от проектов не является
    прямоугольной матрицей с числовыми значениями.
    :raise ProfitValueError: Если значение прибыли отрицательно или убывает
    с ростом инвестиций.
    :return: Словарь с ключами:
    profit - максимально возможная прибыль от инвестиций,
    distribution - распределение инвестиций между проектами.
    """
    validate_matrix(profit_matrix)

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))

def max_profit(mas):
    mas2 = [mas[i][0] for i in range(len(mas))]
    matrix_end = []
    for row in mas:
        new_row = row + [0, 0, 0]
        matrix_end.append(new_row)
    ln = len(mas[0])
    for j in range(1, len(mas[0])):
        h = len(mas) - 1
        while (h >= 0):
            help = [0 for i in range(h + 2)]
            help[h] = mas2[h]
            help[h + 1] = mas[h][j]
            for i in range(h - 1, -1, -1):
                help[i] = mas2[i] + mas[h - i - 1][j]
            mas2[h] = max(help)
            help = []
            h = h - 1

        for i in range(len(mas2)):
            matrix_end[i][ln] = mas2[i]
        ln = ln + 1
    return matrix_end
def get_distribution(matrix_end,profit_max):
    max_profit = matrix_end[-1][-1]
    distribution = [0] * len(profit_max[0])
    for i in range(len(distribution)-1,-1,-1):
        if i != 0 or i != 1:
            predpost= len(matrix_end[0])-2
            if max_profit == matrix_end[-1][predpost]:
                distribution[i] = 0;
                max_profit = matrix_end[-1][predpost]
                break
            predpost = len(matrix_end[0]) - 4
            if max_profit == matrix_end[-1][predpost]:
                distribution[i] = len(profit_max);
                max_profit = matrix_end[-1][predpost]
            for row in range(len(matrix_end)):
                if max_profit == matrix_end[row][predpost]:
                    distribution[i] = 0;
                    max_profit = matrix_end[row][predpost]
                break
        if i != 0 or i!=1:
            predpost = len(matrix_end[0]) - 3
            for row in range(len(matrix_end)):
                if max_profit == matrix_end[row][predpost]:
                    distribution[i] = matrix_end;
                    max_profit = matrix_end[row][predpost]
                break

def validate_matrix(profit_matrix: list[list[int]]) -> \
        dict[str: int, str: list[int]]:
    """Проверяет являться ли таблица прямоугольной матрицей с числовыми значениями
            :param profit_matrix: Таблица значений.
            :raise ValueError: Если таблица прибыли от проектов не является
            прямоугольной матрицей с числовыми значениями."""
    # Проверяем передается таблица или нет
    if not profit_matrix or not profit_matrix[0]:
        raise ValueError(PARAM_ERR_MSG)
    # Проверка на длину строк таблицы
    row_length = len(profit_matrix[0])
    for row in profit_matrix:
        if len(row) != row_length:
            raise ValueError(PARAM_ERR_MSG)
    # Проверяем, что значения числа
    for row in profit_matrix:
        for value in row:
            if not isinstance(value, (int, float)):
                raise ValueError(PARAM_ERR_MSG)
    # Проверяем значение в матрице
    for i, row in enumerate(profit_matrix):
        for j, value in enumerate(row):
            if value < 0:
                raise ProfitValueError(NEG_PROFIT_ERR_MSG, j, i)
            if i > 0 and value < profit_matrix[i - 1][j]:
                raise ProfitValueError(DECR_PROFIT_ERR_MSG, j, i)


def main():
    profit_matrix = [[15, 18, 16, 17],
                     [20, 22, 23, 19],
                     [26, 28, 27, 25],
                     [34, 33, 29, 31],
                     [40, 39, 41, 37]]
    # print(get_invest_distribution(profit_matrix))
    print(profit_matrix)
    print(print_matrix(max_profit(profit_matrix)))


if __name__ == '__main__':
    main()
