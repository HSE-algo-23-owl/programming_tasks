def calculate_determinant(matrix: [[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    check_matrix_exception(matrix)
    if (len(matrix) == 1):
        return matrix[0][0]
    row_index = 0
    det = 0
    for col_index in range(len(matrix)):
        if (matrix[row_index][col_index] == 0):
            continue
        det += (matrix[row_index][col_index] * (-1)**(row_index+col_index) *
                get_minor(matrix, row_index, col_index))
    return det


def check_matrix_exception(matrix):
    if type(matrix) != list:
        raise Exception('Ошибка, задана не матрица')
    if matrix == []:
        raise Exception('Ошибка, пустая матрица')

    for row in matrix:
        if len(matrix) != len(row):
            raise Exception('Ошибка, матрица не квадратная')
def get_minor(matrix, row_index, col_index):
    reduced_matrix = []
    for cur_row_idx, row in enumerate(matrix):
        if cur_row_idx != row_index:
            new_row = []
            for cur_col_idx, col in enumerate(row):
                if cur_col_idx != col_index:
                    new_row.append(col)
            reduced_matrix.append(new_row)
    determinant = calculate_determinant(reduced_matrix)
    return determinant

def main():
    matrix = [[1, 2],
              [3, 4]]
    print('Матрица')
    for row in matrix:
        print(row)

    print(f'Определитель матрицы равен {calculate_determinant(matrix)}')


if __name__ == '__main__':
    main()
