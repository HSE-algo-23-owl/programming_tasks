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
    rows = len(profit_matrix)  # Количество строк (уровней инвестиций)
    cols = len(profit_matrix[0])  # Количество столбцов (проектов)

    # Создаем матрицы для вычисления прибыли и распределения инвестиций
    max_profit_matrix = [[0] * (cols + 1) for _ in range(rows + 1)]
    investment_distribution = [[[] for _ in range(cols + 1)] for _ in range(rows + 1)]
    for idx in range(cols + 1):
        investment_distribution[0][idx] = [0] * idx

    for project_idx in range(1, cols + 1):
        for investment_idx in range(1, rows + 1):
            max_profit = 0
            selected_distribution = []
            for prev_investment_lvl in range(investment_idx + 1):
                current_investment_lvl = investment_idx - prev_investment_lvl
                prev_project_profit = max_profit_matrix[prev_investment_lvl][project_idx - 1]
                if current_investment_lvl == 0:
                    current_project_profit = 0
                else:
                    current_project_profit = profit_matrix[current_investment_lvl - 1][project_idx - 1]
                if prev_project_profit + current_project_profit > max_profit:
                    max_profit = prev_project_profit + current_project_profit
                    previous_project_distribution = investment_distribution[prev_investment_lvl][project_idx - 1]
                    selected_distribution = [*previous_project_distribution, current_investment_lvl]
            max_profit_matrix[investment_idx][project_idx] = max_profit
            investment_distribution[investment_idx][project_idx] = selected_distribution

    # Возвращаем максимальную прибыль и распределение
    return {PROFIT: find_max_profit(profit_matrix), DISTRIBUTION: investment_distribution[-1][-1]}


def find_max_profit(mas):
    """Рассчитывает максимально возможную прибыль
        :param mas: Таблица с распределением прибыли от проектов в
        зависимости от уровня инвестиций. Проекты указаны в столбцах, уровни
        инвестиций в строках.
        :return: Максимальная прибыль
        """
    mas2 = [mas[i][0] for i in range(len(mas))]
    for j in range(1, len(mas[0])):
        h = len(mas) - 1
        while h >= 0:
            help = [0 for i in range(h + 2)]
            help[h] = mas2[h]
            help[h + 1] = mas[h][j]
            for i in range(h - 1, -1, -1):
                help[i] = mas2[i] + mas[h - i - 1][j]
            mas2[h] = max(help)
            help = []
            h = h - 1
    return mas2[len(mas2) - 1]


def validate_matrix(profit_matrix: list[list[int]]):
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
    print(get_invest_distribution(profit_matrix))


if __name__ == '__main__':
    main()
