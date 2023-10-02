
def calculate_determinant(matrix : [[int]]) -> int:
    # Основная процедура получения получения определителя с помощью рекурсии
    validate_matrix_raise_ex(matrix)
    if len(matrix) == 1:
        return matrix[0][0]
    row_idx = get_optimal_row_idx(matrix)
    det = 0
    for col_idx in range (len(matrix[row_idx])):
        if matrix[row_idx][col_idx] == 0:
            continue
        det += (matrix[row_idx][col_idx] * (-1) ** (row_idx + col_idx) *
                calculate_minor(matrix, row_idx, col_idx))
    return det
def calculate_minor(matrix, row_idx, col_idx) -> int:
    # Вычисление минора от матрицы
    reduced_matrix = []
    for i in range(len(matrix) - 1):
        reduced_matrix.append([0] * (len(matrix[i]) - 1))
    for i in range (len(matrix)):
        if i != row_idx:
            for j in range (len(matrix[i])):
                if j != col_idx:
                    if j > col_idx and i > row_idx:
                        reduced_matrix[i-1][j-1] = matrix[i][j]
                    elif j < col_idx and i > row_idx:
                        reduced_matrix[i - 1][j] = matrix[i][j]
                    elif j > col_idx and i < row_idx:
                        reduced_matrix[i][j - 1] = matrix[i][j]
                    else:
                        reduced_matrix[i][j] = matrix[i][j]


    return calculate_determinant(reduced_matrix)

def validate_matrix_raise_ex(matrix):
    # Обработка исключительных ситуаций
    if type(matrix) != list:
        raise Exception("Матрица не введена")
    order = len(matrix)
    for row in matrix:
        if type(row) != list:
            raise Exception ("Введена не матрица")
        if len(row) != order:
            raise Exception("Матрица не квадратная")

def get_optimal_row_idx(matrix):
    # Вычисление оптимальной строки
    maxZeroCounter = 0
    optimalRowIdx = 0
    for i in range (len(matrix)):
        count = 0
        for j in range (len(matrix[i])):
            if matrix[i][j] == 0:
                count = count + 1
        if count >= maxZeroCounter:
            maxZeroCounter = count
            optimalRowIdx = i
    return optimalRowIdx
# Press the green button in the gutter to run the script.

def main():
    matrix = [[1, 2],
              [3, 4]]
    print('Матрица')
    for row in matrix:
        print(row)

    print(f'Определитель матрицы равен {calculate_determinant(matrix)}')


if __name__ == '__main__':
    main()
