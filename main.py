def check_matrix(matrix):
    if type(matrix) != list:
        raise Exception("Error, this non-list type.")
    length = len(matrix)
    if length == 0:
        raise Exception("Error, empty matrix.")
    for row in range(len(matrix)):
        if type(matrix[row]) != list:
            raise Exception("Error, this non-list type.")
        elif len(matrix[row]) != length:
            raise Exception("Error, this is not a square matrix.")


def submatrix(matrix, row, col):
    # Helper function to get the submatrix of a matrix by removing a specific row and column
    return [row[:col] + row[col + 1:] for row in (matrix[:row] + matrix[row + 1:])]


def calculate_determinant(matrix: [[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    if len(matrix) == 1 and len(matrix[0]) == 1:
        return matrix[0][0]

        # Initialize the determinant
    det = 0
    check_matrix(matrix)
    # Iterate through the first row to calculate the determinant
    for col in range(len(matrix[0])):
        # Calculate the cofactor for the current element
        cofactor = matrix[0][col] * calculate_determinant(submatrix(matrix, 0, col))

        # Alternate signs for each element in the first row
        if col % 2 == 1:
            cofactor = -cofactor

        # Add the cofactor to the determinant
        det += cofactor

    return det


def main():
    matrix = [[1, 2],
              [3, 4]]
    print('Матрица')
    for row in matrix:
        print(row)

    print(f'Определитель матрицы равен {calculate_determinant(matrix)}')


if __name__ == '__main__':
    main()
