def calculate_determinant(matrix: [[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    check_matrix(matrix)
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    elif len(matrix) == 1:
        return matrix[0][0]
    row = optimal_row(matrix)
    det = 0
    for col in range(len(matrix[row])):
        det += (-1) ** (row + col) * (calculate_determinant(cut_matrix(matrix, row, col))) * matrix[row][col]
    return det


def check_matrix(matrix: [[int]]):
    if len(matrix) != len(matrix[0]):
        raise Exception("Матрица неквадратная")
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if type(matrix[i][j]) != int:
                raise Exception("Матрица c пустыми элементами")


def optimal_row(matrix: [[int]]) -> int:
    max_count = 0
    zero_count = 0
    id = 0
    for i in range(len(matrix)):
        zero_count = 0
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                zero_count += 1
        if max_count < zero_count:
            max_count = zero_count
            id = i
    return id


def cut_matrix(matrix: [[int]], row, col) -> [[int]]:
    new_matrix = [[0] * (len(matrix) - 1) for _ in range(len(matrix) - 1)]
    for i in range(row):
        for j in range(col):
            new_matrix[i][j] = matrix[i][j]
        for j in range(col + 1, len(matrix)):
            new_matrix[i][j - 1] = matrix[i][j]
    for i in range(row + 1, len(matrix)):
        for j in range(col):
            new_matrix[i - 1][j] = matrix[i][j]
        for j in range(col + 1, len(matrix)):
            new_matrix[i - 1][j - 1] = matrix[i][j]
    return new_matrix


def main():
    matrix = [[1, 2],
              [3, 4]]
    print('Матрица')
    for row in matrix:
        print(row)

    print(f'Определитель матрицы равен {calculate_determinant(matrix)}')


if __name__ == '__main__':
    main()
