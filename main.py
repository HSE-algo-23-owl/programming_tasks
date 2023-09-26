def varidate_matrix_raise(matrix):
    if type(matrix) != list:
        raise Exception("error")
    order = len(matrix)
    if order == 0:
        raise Exception("error")
    for row in matrix:
        if type(row) != list:
            raise Exception("error")
        if len(row) != order:
            raise Exception("error")


def get_optimal_row_idx(matrix):
    length = len(matrix)
    mx = -10
    indmx = 0
    for i in range(length):
        m1 = matrix[i]
        zero_count = 0
        for x in m1:
            if x == 0:
                zero_count += 1
        if mx < zero_count:
            mx = zero_count
            indmx = i
#
    return indmx


def calculate_minor(matrix, i, j):
    return [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]


def calculate_determinant(matrix: [[int]]) -> int:
    varidate_matrix_raise(matrix)

    row_idx = get_optimal_row_idx(matrix)

    if len(matrix) == 1:
        return matrix[0][0]

    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    determinant = 0
    for col_idx in range(len(matrix)):
        determinant += ((-1) ** (col_idx+row_idx)) * matrix[row_idx][col_idx] * calculate_determinant(calculate_minor(matrix, row_idx, col_idx))
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
