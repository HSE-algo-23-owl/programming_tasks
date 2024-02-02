# from _typeshed import SupportsDunderLT, SupportsDunderGT
# from typing import Tuple, List, Any, Dict
from typing import List

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


def __validate_params_raises_ex(profit_matrix):
    # test_none
    if profit_matrix is None:
        raise ValueError(PARAM_ERR_MSG)

    # test_empty
    if len(profit_matrix) == 0:
        raise ValueError(PARAM_ERR_MSG)

    # test_empty_row
    if len(profit_matrix[0]) == 0:
        raise ValueError(PARAM_ERR_MSG)

    # test_incorrect_values
    for row_idx in range(len(profit_matrix)):
        for col_idx in range(len(profit_matrix[row_idx])):
            if type(profit_matrix[row_idx][col_idx]) != int:
                raise ValueError(PARAM_ERR_MSG)
    # test_jag
    for row_idx in range(1, len(profit_matrix)):
        if len(profit_matrix[row_idx - 1]) != len(profit_matrix[row_idx]):
            raise ValueError(PARAM_ERR_MSG)

    # test_negative_profit
    for row_idx in range(len(profit_matrix)):
        for col_idx in range(len(profit_matrix[row_idx])):
            if profit_matrix[row_idx][col_idx] < 0:
                raise ProfitValueError(NEG_PROFIT_ERR_MSG, col_idx, row_idx)

    # test_non_decreasing_sequence
    nar = list(map(list, zip(*profit_matrix)))
    for i in range(len(nar)):
        if nar[i] != sorted(nar[i]):
            raise ProfitValueError(DECR_PROFIT_ERR_MSG, col_idx-1, row_idx)


def __get_max_profit(matrix_to_solve: list[list[int]]) -> int:
    """
    Рассчитывает максимально возможную прибыль нескольких проектов.
    Инвестиции распределяются кратными частями.
    :param matrix_to_solve: Таблица с распределением прибыли от проектов в
    зависимости от уровня инвестиций. Проекты указаны в строках, уровни
    инвестиций в столбцах. Она уменьшается в каждой итерации, в итоге становится массив,
    последнюю ячейку которого мы выводим как результат.
    :return matrix_to_solve[0][-1]: Число - максимальная прибыли при инвестировании
    """
    firms_cnt = len(matrix_to_solve)
    invest_rating_cnt = len(matrix_to_solve[0])
    dict_changing_data = {}
    for i in range(-1, invest_rating_cnt):
        dict_changing_data[i + 1] = 0
    for _ in range(firms_cnt - 1):
        temp_result = __solving_max_profit_of_two(matrix_to_solve[0:1 + 1], dict_changing_data)
        matrix_to_solve[1] = list(temp_result.values())[1:]
        matrix_to_solve.pop(0)
        dict_changing_data = temp_result
    return matrix_to_solve[0][-1]


def __solving_max_profit_of_two(two_inw_arr: list[list[int]], dict_changing_data: dict[int, int]) -> dict[int, int]:
    """
    Рассчитывает максимально возможную прибыль по двум проектам.
    Инвестиции распределяются кратными частями.
    :param two_inw_arr: Таблица с распределением прибыли от проектов в
    зависимости от уровня инвестиций. Проекты указаны в строках, уровни
    инвестиций в столбцах.
    :param dict_changing_data: Словарь с начальными данными инвестированием в
    сравниваемые проекты в прошлом
    :return dict_changing_data: Словарь с правильным и измененными данными по
    инвестированию в сравниваемые проекты
    """
    # two_inw_arr =
    a = 0
    b = 0
    invest_rating_cnt = len(two_inw_arr[0])
    for vl_a_pr in range(0, invest_rating_cnt + 1):
        for all_inp in range(vl_a_pr, invest_rating_cnt + 1):
            vl_b_pr = all_inp - vl_a_pr
            summ = 0
            if vl_a_pr == 0:
                if vl_b_pr != 0:
                    summ = two_inw_arr[1][vl_b_pr - 1]
            else:
                if vl_b_pr == 0:
                    summ = two_inw_arr[0][vl_a_pr - 1]
                else:
                    summ = two_inw_arr[0][vl_a_pr - 1] + two_inw_arr[1][vl_b_pr - 1]
            if dict_changing_data[all_inp] < summ:
                dict_changing_data[all_inp] = summ
                a = vl_a_pr
                b = vl_b_pr
    return dict_changing_data


def __generate_combinations_recursive(array, n, current=None, target_sum=None):
    if current is None:
        current = []
    if n == 0:
        if sum(current) == target_sum:
            return [current]
        return []

    result = []
    for num in array:
        result.extend(__generate_combinations_recursive(array, n - 1, current + [num], target_sum))

    return result


def __generate_combinations_with_sum(range_start, range_end, length):
    array = list(range(range_start, range_end + 1))
    return __generate_combinations_recursive(array, length, target_sum=range_end)


def __get_distributions(profit_matrix: list[list[int]], max_investments: int) -> list[int]:
    """
    Рассчитывает комбинацию с максимально возможной прибылью (распределение инвестиций
    между несколькими проектами). Инвестиции распределяются кратными частями.
    :param profit_matrix: Изначально данная нам матрица инвестиций
    :param max_investments: Максимально возможная прибыль
    :return combination: Комбинация, которая нам нужна
    """
    cnt_proj_to_inv = len(profit_matrix[0])  # 4 количество проектов
    vars_to_inv = len(profit_matrix)  # 5 варианты вложения
    all_combinations = __generate_combinations_with_sum(0, vars_to_inv, cnt_proj_to_inv)

    # j - индекс элемента {0,1,2,3}, combination[j] - значение элемента {0,1,2,3,4,5}
    for combination in all_combinations:
        sum_combination = 0
        for j in range(len(combination)):
            if combination[j] != 0:
                sum_combination += profit_matrix[combination[j] - 1][j]
        if sum_combination == max_investments:
            return combination


def get_invest_distribution(profit_matrix: list[list[int]]) -> dict[str: int, str: list[int]]:
    """
    Рассчитывает максимально возможную прибыль. Инвестиции распределяются кратными частями.
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
    __validate_params_raises_ex(profit_matrix)
    max_profit = __get_max_profit(list(map(list, zip(*profit_matrix))))
    distributions = __get_distributions(profit_matrix, max_profit)

    return {PROFIT: max_profit, DISTRIBUTION: distributions}


def main():
    profit_matrix = [[5, 7, 2, 10],
                     [9, 8, 4, 15],
                     [11, 10, 5, 16],
                     [12, 12, 8, 17],
                     [14, 15, 9, 18]]
    print(get_invest_distribution(profit_matrix))


if __name__ == '__main__':
    main()
