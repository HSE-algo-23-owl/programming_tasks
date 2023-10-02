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
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0
    for col_idx in range(len(matrix)):
        det += matrix[0][col_idx] * (-1) ** col_idx * calculate_determinant([matrix[i][:col_idx] + matrix[i][col_idx + 1:] for i in range(1, len(matrix))])
    return det


'''def calculate_minor(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]'''



def check_matrix_raises_ex(matrix: [[int]]):
    """Проверяет, можно ли вычислить определитель у данной матрицы
        :param matrix: матрица, которую ввел пользователь
        :raise Exception: если значение параметра не является целочисленной
        квадратной матрицей
        """
    if matrix[0] is None:
        raise Exception("Нельзя передавать пустой список в матрицу!")
    if type(matrix) != list:
        raise Exception('Матрица не того формата')
    order = len(matrix)
    for row in matrix:
        if type(row) != list:
            raise Exception('Матрица не того формата')
        if len(row) != order:
            raise Exception('Матрица должна быть квадратной!')


def main():
    matrix = [[1, 2],
              [3, 4]]
    print('Матрица')
    for row in matrix:
        print(row)

    print(f'Определитель матрицы равен {calculate_determinant(matrix)}')


if __name__ == '__main__':
    main()

