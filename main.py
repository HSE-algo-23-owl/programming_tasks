def is_suitable_matrix(matrix):
    if type(matrix) != list or len(matrix) == 0:
        raise Exception('Вы ввели не матрицу')
    matrix_dimension = len(matrix)
    for row in matrix:
        if type(row) != list:
            raise Exception('Ваша матрица содержит разные типы данных')
        if len(row) != matrix_dimension:
            raise Exception('Вы ввели не квадратную матрицу')
        if None in row:
            raise Exception('У вас None в строке))')

def reduced_matrix(matrix, i, j):
    tmp = []
    bb = []
    for k in range(len(matrix)):
        tmp.clear()
        for s in range(len(matrix)):
            if i != k and s != j:
                tmp.append(matrix[k][s])
        if len(tmp) > 0:
            bb.append([int(x) for x in tmp])
    return bb


def calculate_determinant(matrix: [[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы"""
    is_suitable_matrix(matrix)
    ans = 0
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    for i in range(len(matrix)):
        ans += (-1) ** i * matrix[i][0] * calculate_determinant(reduced_matrix(matrix, i, 0))
    return ans


def main():
    matrix = []
    print('Матрица')
    for row in matrix:
        print(row)

    print(f'Определитель матрицы равен {calculate_determinant(matrix)}')


if __name__ == '__main__':
    main()
