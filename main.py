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
    __validate_params_raises_ex(profit_matrix)
    count_proj = len(profit_matrix[0])
    count_invest = len(profit_matrix)

    profit = [[0 for _ in range(count_proj + 1)] for _ in range(count_invest + 1)]
    distr = [[[] for _ in range(count_proj + 1)] for _ in range(count_invest + 1)]
    for col_idx in range(len(distr[0])):
        distr[0][col_idx] = [0]*col_idx

    for proj_idx in range(1, count_proj + 1):
        for inv_idx in range(1, count_invest + 1):
            max_profit = 0
            temp_distr = []
            for prev_inv_lvl in range(inv_idx + 1):
                cur_inv_lvl = inv_idx - prev_inv_lvl
                prev_proj_profit = profit[prev_inv_lvl][proj_idx - 1]
                cur_proj_profit = 0 if cur_inv_lvl == 0 else profit_matrix[cur_inv_lvl - 1][proj_idx - 1]
                if prev_proj_profit + cur_proj_profit > max_profit:
                    max_profit = prev_proj_profit + cur_proj_profit
                    prev_proj_distr = distr[prev_inv_lvl][proj_idx - 1]
                    temp_distr = [*prev_proj_distr, cur_inv_lvl]
            profit[inv_idx][proj_idx] = max_profit
            distr[inv_idx][proj_idx] = temp_distr

    return {PROFIT: profit[-1][-1], DISTRIBUTION: distr[-1][-1]}


def __validate_params_raises_ex(profit_matrix):
    if profit_matrix == None or len(profit_matrix) == 0 or any(len(row) == 0 for row in profit_matrix):
        raise ValueError(PARAM_ERR_MSG)
    if not all(isinstance(value, int) and value is not None for row in profit_matrix for value in row):
        raise ValueError(PARAM_ERR_MSG)

    for row_idx, row in enumerate(profit_matrix):
        for project_idx, value in enumerate(row):
            if row_idx > 0 and value < profit_matrix[row_idx - 1][project_idx]:
                raise ProfitValueError(DECR_PROFIT_ERR_MSG, project_idx, row_idx)
            if value < 0:
                raise ProfitValueError(NEG_PROFIT_ERR_MSG, project_idx, row_idx)


def main():
    matrix = [[15, 18, 16, 17],
              [20, 22, 23, 19],
              [26, 28, 27, 25],
              [34, 33, 29, 31],
              [40, 39, 41, 37]]
    print(get_invest_distribution(matrix))


if __name__ == '__main__':
    main()
