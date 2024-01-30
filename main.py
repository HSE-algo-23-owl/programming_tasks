PROFIT = 'profit'
DISTRIBUTION = 'distribution'
PARAM_ERR_MSG = ('Таблица прибыли от проектов не является прямоугольной '
                 'матрицей с числовыми значениями')
NEG_PROFIT_ERR_MSG = 'Значение прибыли не может быть отрицательно'
DECR_PROFIT_ERR_MSG = 'Значение прибыли не может убывать с ростом инвестиций'

from copy import deepcopy


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
    validate_matrix_exc(profit_matrix)
    max_profit_matrix = get_max_profit_matrix(profit_matrix)
    # Дополним ведущими нулями
    ans = max_profit_matrix[-1][-1]
    ans[DISTRIBUTION] = (len(profit_matrix[0])-(len(ans[DISTRIBUTION])))*[0]+ans[DISTRIBUTION]
    return max_profit_matrix[-1][-1]


def validate_matrix_exc(profit_matrix):
    if profit_matrix is None:
        raise ValueError("Таблица прибыли от проектов не является прямоугольной матрицей с числовыми значениями")
    if not profit_matrix:
        raise ValueError("Таблица прибыли от проектов не является прямоугольной матрицей с числовыми значениями")
    for levels in range(len(profit_matrix)):
        if not profit_matrix[0]:
            raise ValueError("Таблица прибыли от проектов не является прямоугольной матрицей с числовыми значениями")
        if len(profit_matrix[0]) != len(profit_matrix[levels]):
            raise ValueError("Таблица прибыли от проектов не является прямоугольной матрицей с числовыми значениями")

        for project in range(len(profit_matrix[levels])):
            if type(profit_matrix[levels][project]) != int:
                raise ValueError("Таблица прибыли от проектов не является прямоугольной матрицей с числовыми значениями")
            if profit_matrix[levels][project] < 0:
                raise ProfitValueError('Значение прибыли не может быть отрицательно',project, levels)
            if levels > 0 and profit_matrix[levels - 1][project] > profit_matrix[levels][project]:
                raise ProfitValueError('Значение прибыли не может убывать с ростом инвестиций',project, levels)


def get_max_profit_matrix(profit_matrix):
    level_len = len(profit_matrix)
    proj_len = len(profit_matrix[0])
    max_profit_matrix = [[{PROFIT: 0, DISTRIBUTION: []}
                          for _ in range(proj_len+1)]
                         for _ in range(level_len+1)]

    for project_id in range(1, proj_len+1):
        for level_id in range(1, level_len+1):
            # Берем все из предыдущего
            max_profit_dict = deepcopy(max_profit_matrix[level_id][project_id-1])
            max_profit_dict[DISTRIBUTION] += [0]

            # Смотрим, если бы брали не все, а только часть
            for prev_level in range(level_id):
                prev_profit = max_profit_matrix[prev_level][project_id - 1][PROFIT]
                cur_level = level_id-prev_level
                cur_profit = profit_matrix[cur_level - 1][project_id - 1]
                total_profit = prev_profit+cur_profit

                if total_profit > max_profit_dict[PROFIT]:
                    max_profit_dict[PROFIT] = total_profit
                    max_profit_dict[DISTRIBUTION] = max_profit_matrix[prev_level][project_id - 1][DISTRIBUTION] + [cur_level]
            max_profit_matrix[level_id][project_id] = max_profit_dict
    return max_profit_matrix


def main():
    profit_matrix = [[15, 18, 16, 17],
                     [20, 22, 23, 19],
                     [26, 28, 27, 25],
                     [34, 33, 29, 31],
                     [40, 39, 41, 37]]
    print(get_invest_distribution(profit_matrix))


if __name__ == '__main__':
    main()
