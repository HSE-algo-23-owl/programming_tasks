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
    __validate_params_raises_ex(profit_matrix)
    max_profit_matrix = __get_max_profit_matrix(profit_matrix)
    max_profit = max_profit_matrix[-1][-1][PROFIT]
    distributions = max_profit_matrix[-1][-1][DISTRIBUTIONS]
    return {PROFIT: max_profit, DISTRIBUTIONS: distributions}


def __validate_params_raises_ex(profit_matrix):
    if profit_matrix is None:
        raise ValueError(PARAM_ERR_MSG)
    if (len(profit_matrix) == 0):
        raise ValueError(PARAM_ERR_MSG)
    if (len(profit_matrix[0]) == 0):
        raise ValueError(PARAM_ERR_MSG)
    for row in range(len(profit_matrix)):
        for col in range(len(profit_matrix[row])):
            if type(profit_matrix[row][col]) != int:
                raise ValueError(PARAM_ERR_MSG)
    for i in range(len(profit_matrix) - 1):
        if len(profit_matrix[i]) != len(profit_matrix[i + 1]):
            raise ValueError(PARAM_ERR_MSG)
    for row in range(len(profit_matrix)):
        for columns in range(len(profit_matrix[row])):
            if profit_matrix[row][columns] < 0:
                raise ProfitValueError(NEG_PROFIT_ERR_MSG, columns, row)
    for rows in range(len(profit_matrix)-1):
        for cols in range(len(profit_matrix[rows])):
            if profit_matrix[rows][cols] > profit_matrix[rows+1][cols]:
                raise ProfitValueError(DECR_PROFIT_ERR_MSG, cols, rows+1)

def __get_max_profit_matrix(profit_matrix):
    level_cnt = len(profit_matrix) + 1
    proj_cnt = len(profit_matrix[0]) + 1
    max_profit_matrix = [
        [
            {PROFIT: 0, DISTRIBUTIONS: [[]]} for _ in range(proj_cnt)
        ] for _ in range(level_cnt)
    ]
    for column in range(len(max_profit_matrix[0])):
        max_profit_matrix[0][column][DISTRIBUTIONS] = [[0] * column]

    for proj_idx in range(1, proj_cnt):
        for level_idx in range(1, level_cnt):
            for prev_level in range(level_idx + 1):
                cur_level = level_idx - prev_level
                prev_profit = max_profit_matrix[prev_level][proj_idx - 1][PROFIT]
                cur_profit = 0 if cur_level == 0 else profit_matrix[cur_level - 1][proj_idx - 1]
                if prev_profit + cur_profit > max_profit_matrix[level_idx][proj_idx][PROFIT]:
                    max_profit_matrix[level_idx][proj_idx][PROFIT] = prev_profit + cur_profit
                    max_profit_matrix[level_idx][proj_idx][DISTRIBUTIONS] = [
                        dist + [cur_level] for dist in max_profit_matrix[prev_level][proj_idx - 1][DISTRIBUTIONS]
                    ]
                elif prev_profit + cur_profit == max_profit_matrix[level_idx][proj_idx][PROFIT]:
                    max_profit_matrix[level_idx][proj_idx][DISTRIBUTIONS] += [
                        dist + [cur_level] for dist in max_profit_matrix[prev_level][proj_idx - 1][DISTRIBUTIONS]
                    ]
    return max_profit_matrix

def main():
    profit_matrix = [[1, 2, 2],
                  [3, 5, 4],
                  [7, 6, 5]]
    print(get_invest_distributions(profit_matrix))


if __name__ == '__main__':
    main()
