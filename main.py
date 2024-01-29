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


# Функция для проверки матрицы на корректность
def check_profit_matrix(profit_matrix):
    # Проверка на None, пустой список и некорректные значения
    if profit_matrix is None or len(profit_matrix) == 0 or any(len(row) == 0 for row in profit_matrix):
        raise ValueError(PARAM_ERR_MSG)
    if not all(isinstance(value, int) and value is not None for row in profit_matrix for value in row):
        raise ValueError(PARAM_ERR_MSG)

    # Проверка на возрастание прибыли от уровня к уровню и отрицательные знач.
    for i, row in enumerate(profit_matrix):
        for j, value in enumerate(row):
            if value < 0:
                raise ProfitValueError(NEG_PROFIT_ERR_MSG, j, i)
            if i > 0 and value < profit_matrix[i - 1][j]:
                raise ProfitValueError(DECR_PROFIT_ERR_MSG, j, i)



def get_invest_distribution(profit_matrix: list[list[int]]) -> dict[str: int, str: list[int]]:
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

    # Проверка матрицы на корректность
    check_profit_matrix(profit_matrix)

    num_projects = len(profit_matrix[0])
    num_investment_levels = len(profit_matrix)

    dp = [[0 for _ in range(num_investment_levels + 1)] for _ in range(num_projects + 1)]
    invest_distribution = [[0 for _ in range(num_investment_levels + 1)] for _ in range(num_projects + 1)]

    # Рекурсивная функция для расчета максимальной прибыли и распределения инвестиций
    def _get_invest_distribution(i, j):
        if i == 0 or j == 0:
            return 0

        max_profit = 0
        best_level = 0
        for k in range(min(j, num_investment_levels) + 1):
            current_profit = profit_matrix[k - 1][i - 1] + _get_invest_distribution(i - 1, j - k) if k > 0 else _get_invest_distribution(i - 1, j)
            if current_profit > max_profit:
                max_profit = current_profit
                best_level = k

        dp[i][j] = max_profit
        invest_distribution[i][j] = best_level

        return max_profit

    _get_invest_distribution(num_projects, num_investment_levels)

    final_distribution = [0] * num_projects
    remaining_investment = num_investment_levels
    for i in range(num_projects, 0, -1):
        final_distribution[i - 1] = invest_distribution[i][remaining_investment]
        remaining_investment -= final_distribution[i - 1]

    return {PROFIT: dp[num_projects][num_investment_levels], DISTRIBUTION: final_distribution}

def main():
    profit_matrix = [[15, 18, 16, 17],
                     [20, 22, 23, 19],
                     [26, 28, 27, 25],
                     [34, 33, 29, 31],
                     [40, 39, 41, 37]]
    print(get_invest_distribution(profit_matrix))


if __name__ == '__main__':
    main()
