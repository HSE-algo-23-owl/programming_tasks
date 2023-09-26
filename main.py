def calculate_determinant(matrix: [[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    check_matrix_raises_ex(matrix)
    if len(matrix) == 1:
        return matrix[0][0]

    row_idx = get_max_zero_row_idx(matrix)
    det = 0
    for col_idx in range(len(matrix)):
        if matrix[row_idx][col_idx] == 0:
            continue
        det += (matrix[row_idx][col_idx] * (-1)**(row_idx * col_idx) *
                calculate_minor(matrix, row_idx, col_idx))
    return det

def get_max_zero_row_idx(matrix) -> int:
    pass

def calculate_minor(matrix, row_idx, col_idx) -> int:
    pass

def check_matrix_raises_ex(matrix):
    if type(matrix) != list:
        raise Exception('Ошибка!')
    order = len(matrix)
    for row in matrix:
        if type(row) != list:
            raise Exception('Ошибка 123')
        if len(row) != order:
            raise Exception

    if len(matrix) == 1:
        return matrix[0][0]

def main():
    matrix = [[1, 2],
              [3, 4]]
    print('Матрица')
    for row in matrix:
        print(row)

    print(f'Определитель матрицы равен {calculate_determinant(matrix)}')


if __name__ == '__main__':
    main()
