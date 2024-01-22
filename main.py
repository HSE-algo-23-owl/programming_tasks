INF = float('inf')
COST = 'cost'
PATH = 'path'
PARAM_ERR_MSG = ('Таблица цен не является прямоугольной матрицей с '
                 'числовыми значениями')


def get_min_cost_path(price_table: list[list[float | int]]) -> \
        dict[str: float, str: list[tuple[int, int]]]:
    __validate_params_raises_ex(price_table)
    cost_tbl = __get_cost_tbl(price_table)
    if cost_tbl[-1][-1] == INF or price_table[0][0] is None:
        return {COST: None, PATH: None}
    else:
        path_back = __get_path_back(cost_tbl)
        return {COST: cost_tbl[-1][-1], PATH: path_back[::-1]}


def __get_path_back(cost_tbl):
    cur_row = len(cost_tbl) - 1
    cur_col = len(cost_tbl[0]) - 1
    path_back = [(cur_row - 1, cur_col - 1)]
    while cur_row > 1 or cur_col > 1:
        cost_up = cost_tbl[cur_row - 1][cur_col]
        cost_left = cost_tbl[cur_row][cur_col - 1]
        if cost_up <= cost_left:
            cur_row -= 1
        else:
            cur_col -= 1
        path_back.append((cur_row - 1, cur_col - 1))
    return path_back


def __validate_params_raises_ex(allow_table):
    if allow_table is None:
        raise ValueError(PARAM_ERR_MSG)
    if not allow_table:
        raise ValueError(PARAM_ERR_MSG)
    for i in range(len(allow_table)):
        if not allow_table[i]:
            raise ValueError(PARAM_ERR_MSG)
        if len(allow_table[0]) != len(allow_table[i]):
            raise ValueError(PARAM_ERR_MSG)
        for j in range(len(allow_table[i])):
            if allow_table[i][j] is None or type(allow_table[i][j]) == float or type(allow_table[i][j]) == int:
                continue
            else:
                raise ValueError(PARAM_ERR_MSG)


def __get_cost_tbl(price_table):
    col_cnt = len(price_table[0]) + 1
    row_cnt = len(price_table) + 1
    cost_tbl = [[INF] * col_cnt for _ in range(row_cnt)]
    cost_tbl[1][1] = price_table[0][0]
    for row_idx in range(1, row_cnt):
        for col_idx in range(1, col_cnt):
            if row_idx == col_idx == 1:
                continue
            if price_table[row_idx - 1][col_idx - 1] is None:
                cost_tbl[row_idx][col_idx] = INF
                continue
            cost_up = cost_tbl[row_idx - 1][col_idx]
            cost_left = cost_tbl[row_idx][col_idx - 1]
            cost_tbl[row_idx][col_idx] = price_table[row_idx - 1][col_idx - 1] + min(cost_up, cost_left)
    return cost_tbl


def main():
    table = [[1, 2, 2],
             [3, None, 2],
             [None, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == '__main__':
    main()
