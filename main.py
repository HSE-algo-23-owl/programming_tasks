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
    values = __get_max_profit_matrix(profit_matrix)
    max_values = values[-1][-1][PROFIT]
    distributions = values[-1][-1][DISTRIBUTIONS]
    return {PROFIT: max_values, DISTRIBUTIONS: distributions}


def __get_max_profit_matrix(profit_matrix):
    __validate_matrix(profit_matrix)
    a = len(profit_matrix) + 1
    t = len(profit_matrix[0]) + 1
    ans = [[{PROFIT: 0, DISTRIBUTIONS: [[]]} for _ in range(t)] for _ in range(a)]

    for i in range(len(ans[0])):
        ans[0][i][DISTRIBUTIONS] = [[0] * i]

    for i in range(1, t):
        for j in range(1, a):
            for k in range(j + 1):
                cur = j - k
                prev = ans[k][i - 1][PROFIT]
                cur1 = 0 if cur == 0 else profit_matrix[cur - 1][i - 1]
                if prev + cur1 == ans[j][i][PROFIT]:
                    ans[j][i][DISTRIBUTIONS] += [dist + [cur] for dist in ans[k][i - 1][DISTRIBUTIONS]]
                elif prev + cur1 > ans[j][i][PROFIT]:
                    ans[j][i][PROFIT] = prev + cur1
                    ans[j][i][DISTRIBUTIONS] = [dist + [cur] for dist in ans[k][i - 1][DISTRIBUTIONS]]
    return ans


def __validate_matrix(matrix):
    if matrix is None:
        raise ValueError(PARAM_ERR_MSG)
    if len(matrix) == 0:
        raise ValueError(PARAM_ERR_MSG)
    if len(matrix[0]) == 0:
        raise ValueError(PARAM_ERR_MSG)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if type(matrix[i][j]) != int:
                raise ValueError(PARAM_ERR_MSG)
    for i in range(1, len(matrix)):
        if len(matrix[i]) != len(matrix[i - 1]):
            raise ValueError(PARAM_ERR_MSG)
    for i in range(len(matrix)-1):
        for j in range(len(matrix[i])):
            if matrix[i][j] > matrix[i + 1][j]:
                raise ProfitValueError(DECR_PROFIT_ERR_MSG, j, i + 1)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] < 0:
                raise ProfitValueError(NEG_PROFIT_ERR_MSG, j, i)


def main():
    profit_matrix = [[1, 1, 1],
                     [2, 2, 2],
                     [3, 3, 3]]
    print(get_invest_distributions(profit_matrix))


if __name__ == '__main__':
    main()
