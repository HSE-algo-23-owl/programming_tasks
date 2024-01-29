PROFIT = 'profit'
DISTRIBUTIONS = 'distributions'
PARAM_ERR_MSG = ('Таблица прибыли от проектов не является прямоугольной '
                 'матрицей с числовыми значениями')
NEG_PROFIT_ERR_MSG = 'Значение прибыли не может быть отрицательно'
DECR_PROFIT_ERR_MSG = 'Значение прибыли не может убывать с ростом инвестиций'


class ProfitValueError(Exception):
    def __init__(self, message, project_idx, row_idx):
        self.project_idx = project_idx
        self.row_idx = row_idx
        super().__init__(message)


def get_invest_distributions(profit_matrix: list[list[int]]) -> \
        dict[str: int, str: list[list[int]]]:
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
    distributions - списком со всеми вариантами распределения инвестиций между
    проектами, обеспечивающими максимальную прибыль.
    """
    __validate_data_raises_ex(profit_matrix)
    max_profit = __get_max_profit(profit_matrix)
    distributions = __get_distributions(profit_matrix)

    return {PROFIT: max_profit, DISTRIBUTIONS: distributions}


def __get_distributions(profit_matrix: list[list[int]]) -> list[list[int]]:
    """Вспомогательная приватная функция для расчета всех способов инвестиций
    между несколькими проектами. Инвестиции распределяются кратными частями.
    :param profit_matrix: Таблица с распределением прибыли от проектов в
    зависимости от уровня инвестиций. Проекты указаны в столбцах, уровни
    инвестиций в строках.
    :return: distributions - списком со всеми вариантами распределения инвестиций между
    проектами, обеспечивающими максимальную прибыль.
    """
    if len(profit_matrix[0]) == 1:
        return [profit_matrix[0]]

    row_cnt = len(profit_matrix)  # варианты вложения
    col_cnt = len(profit_matrix[0])  # количество проектов

    profit_matrix_extend = [[0]*col_cnt] + [[*i] for i in profit_matrix]  # генерация расширенной матрицы
    profit_matrix_all = [[{PROFIT: 0, DISTRIBUTIONS: []} for _ in range(col_cnt)] for _ in range(row_cnt+1)]

    for cur_col_idx in range(col_cnt - 1, 0, -1):  # номер проекта
        for cur_row_idx in range(row_cnt - 1, -1, -1):  # шаг, строка, возможная сумма распределения
            current_item_dict = profit_matrix_all[cur_row_idx+1][cur_col_idx-1]
            for start_level_idx in range(cur_row_idx + 1 + 1):  # уровни проектов
                end_level_idx = cur_row_idx - start_level_idx + 1

                if cur_col_idx == col_cnt - 1:
                    s = profit_matrix_extend[start_level_idx][cur_col_idx-1] + profit_matrix_extend[end_level_idx][cur_col_idx]
                    if s > current_item_dict[PROFIT]:
                        current_item_dict[PROFIT] = s
                        current_item_dict[DISTRIBUTIONS] = [[start_level_idx, end_level_idx]]

                    elif s == current_item_dict[PROFIT]:
                        current_item_dict[PROFIT] = s
                        current_item_dict[DISTRIBUTIONS].append([start_level_idx, end_level_idx])
                    continue

                prev_distributions = profit_matrix_all[end_level_idx][cur_col_idx][DISTRIBUTIONS]
                s = profit_matrix_extend[start_level_idx][cur_col_idx-1] + profit_matrix_all[end_level_idx][cur_col_idx][PROFIT]

                if s < current_item_dict[PROFIT]:  # нам такие случаи неинтересны
                    continue

                if s > current_item_dict[PROFIT]:  # если мы находим профит больше текущего, то сбрасываем распределение
                    current_item_dict[PROFIT] = s
                    current_item_dict[DISTRIBUTIONS] = []

                if s == current_item_dict[PROFIT]:  # если нашли равный элемент, то добавляем сумма вложения в распределение
                    current_item_dict[PROFIT] = s
                    current_item_dict[DISTRIBUTIONS] = [i for i in current_item_dict[DISTRIBUTIONS]]

                for item in prev_distributions:  # переносим предыдущие распределение в новое
                    current_item_dict[DISTRIBUTIONS].append([start_level_idx] + item)
                if not prev_distributions: # если отсутствуют, то заполняем нулями
                    current_item_dict[DISTRIBUTIONS].append([start_level_idx] + [0]*(col_cnt-cur_col_idx))

    return profit_matrix_all[row_cnt][0][DISTRIBUTIONS]


def __get_max_profit(profit_matrix: list[list[int]]) -> int:
    """Вспомогательная приватная функция для расчета максимального профита.
    :param profit_matrix: Таблица с распределением прибыли от проектов в
    зависимости от уровня инвестиций. Проекты указаны в столбцах, уровни
    инвестиций в строках.
    :return: максимальный профит
    """
    row_cnt = len(profit_matrix)
    max_profit = profit_matrix[0][0]

    temp_matrix = [[*row] for row in profit_matrix]

    for project_col_idx in range(len(temp_matrix[0]) - 1):
        temp_lst = []  # вспомогательный список для хранения максимальных значений
        for project_row_idx in range(len(temp_matrix)):
            max_value = 0
            for start_idx in range(project_row_idx + 2):
                end_idx = project_row_idx - start_idx + 1

                if start_idx == 0:
                    if max_value < temp_matrix[end_idx - 1][project_col_idx + 1]:
                        max_value = temp_matrix[end_idx - 1][project_col_idx + 1]
                    continue

                if end_idx == 0:
                    if max_value < temp_matrix[start_idx - 1][project_col_idx]:
                        max_value = temp_matrix[start_idx - 1][project_col_idx]
                    continue

                if max_value < temp_matrix[start_idx-1][project_col_idx] + temp_matrix[end_idx-1][project_col_idx+1]:
                    max_value = temp_matrix[start_idx-1][project_col_idx] + temp_matrix[end_idx-1][project_col_idx+1]

            temp_lst.append(max_value)

        for i in range(len(temp_lst)):
            temp_matrix[i][project_col_idx + 1] = temp_lst[i]

    return temp_matrix[-1][-1]


def __validate_data_raises_ex(profit_matrix: any):
    """Валидация таблицы и данных, содержащихся в ней.
    :param profit_matrix: Таблица с распределением прибыли от проектов в
    зависимости от уровня инвестиций. Проекты указаны в столбцах, уровни
    инвестиций в строках.
    :raise ValueError: Если таблица прибыли от проектов не является
    прямоугольной матрицей с числовыми значениями.
    :raise ProfitValueError: Если значение прибыли отрицательно или убывает
    с ростом инвестиций.
    """

    is_error = False

    match profit_matrix:
        case None:
            is_error = True

        case list() as lst if not len(lst):  # если список пуст
            is_error = True

        case [list() as lst] if not len(lst):  # если вложенные списки пусты
            is_error = True

        case list() as lst:
            sublist_len = len(lst[0])

            for row_idx, sublist in enumerate(lst):
                if sublist_len != len(sublist):
                    is_error = True
                    break

                for project_idx, item in enumerate(sublist):
                    if not isinstance(item, int) or item is None:  # проверка на тип
                        raise ValueError(PARAM_ERR_MSG)
                    if item < 0:  # проверка на отрицательные значения
                        raise ProfitValueError(NEG_PROFIT_ERR_MSG, project_idx, row_idx)
                    if row_idx > 0 and item < profit_matrix[row_idx - 1][project_idx]:  # проверка убывающей прибыли
                        raise ProfitValueError(DECR_PROFIT_ERR_MSG, project_idx, row_idx)

    if is_error:
        raise ValueError(PARAM_ERR_MSG)


def main():
    profit_matrix = [[1, 1, 1],
                     [2, 2, 2],
                     [3, 3, 3]]
    print(get_invest_distributions(profit_matrix))


if __name__ == '__main__':
    main()
