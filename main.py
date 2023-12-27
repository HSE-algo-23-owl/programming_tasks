def calculate_determinant(matrix: [int]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы
    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    check_matrix_validate(matrix)
    return calculate_recursion_matrix_determinant(matrix)


def check_matrix_validate(matrix: list[list[int]]):
    """ Функция проверки матрицы
    :param matrix: матрица
    :return: raise Exception если :
     1) Входной параметр None или пустой массив;
     2) Матрица не квардратная;
    """

    if not matrix or matrix is None:
        raise Exception('Error: the matrix is empty!')

    rows = len(matrix)
    for row in matrix:
        if len(row) != rows:
            raise Exception('Error: the matrix is not square!')


def calculate_minor_matrix(matrix: [int], i, j) -> int:
    """Функция расчета минора M ij – определитель ( n − 1 ).
    param: список списков - матрица, type int
    return: возвращает матрицу 2x2
    """
    return [matrix_a[:j] + matrix_a[j + 1:] for matrix_a in (matrix[:i] + matrix[i + 1:])]


def calculate_recursion_matrix_determinant(matrix: list[list[int]]) -> list[list[int]] | int:
    """Рекурсивная функция расчета определителей матриц nxn, через Mij
    param: список списков - матрица, type int
    return: определитель матрицы
    """
    # случай для матрицы 1x1
    if len(matrix) == 1:
        return matrix[0][0]
    # случай расчета входной квадратной матрицы 2x2 и расчета миноров из calculate_minor_matrix
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    # случай расчета детермината для квадратных матриц порядка nxn
    # -1 возводится в степень к, для соблюдения очередности по формуле +-+- (-1) в степени ,
    determinant = 0
    for k in range(len(matrix)):
        determinant += ((-1) ** k) * matrix[0][k] * calculate_recursion_matrix_determinant(
            calculate_minor_matrix(matrix, 0, k))
    return determinant


def main():
    print(f'Определитель матрицы - {calculate_determinant(matrix)}')


if __name__ == '__main__':
    main()


