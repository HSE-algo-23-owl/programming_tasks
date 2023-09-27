def calculate_determinant(matrix: [[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """

    validate_matrix_ex(matrix)  # валидация матрицы
    return calculate_determinant_recursion(matrix)


def calculate_determinant_recursion(matrix: [[int]]) -> int:
    """Вспомогательная функция для вычисления определителя квадратной матрицы методом рекурсии

    :param matrix: целочисленная квадратная матрица
    :return: определитель квадратной матрицы
    """

    if len(matrix) == 1: # база рекурсии (если остался 1 элемент)
        return matrix[0][0]

    idx_optimal_row = get_optimal_row_idx(matrix)  # индекс оптимальной строки
    if idx_optimal_row != 0:
        matrix[0], matrix[idx_optimal_row] = matrix[idx_optimal_row], matrix[0]  # делаем перестановку строки
    matrix_det = 0
    for item_idx, item in enumerate(matrix[0]):  # обход строки, вычисление определителя с помощью алгебраического дополнения
        matrix_det += (-1)**item_idx * item * calculate_determinant_recursion([[new_item for new_item_idx, new_item in enumerate(matrix[row]) if new_item_idx != item_idx] for row in range(1, len(matrix))])
        # редуцирование матрицы осуществляется путем генерации нового списка с исключением вычеркнутых строки и столбца

    return matrix_det


def validate_matrix_ex(matrix: [[int]]) -> None:
    """Вспомогательная функция для валидации матрицы

    :param matrix: целочисленная квадратная матрица
    :raises Exception: если матрица не является квадратной или содержит элементы других типов данных
    """

    if type(matrix) != list:
        raise Exception("Ошибка! Функция принимает только списки")
    if not any(matrix) or None in matrix:
        raise Exception("Ошибка! Матрица не должна быть пустой")

    column_count = len(matrix)
    for row in matrix:
        if len(row) != column_count or type(row) != list:
            raise Exception("Ошибка! Матрица должна быть квадратной")
        for item in row:  # обход элементов строки
            if type(item) != int:  # если в строке имеется элемент, отличающийся от типа int
                raise Exception("Ошибка! Матрица может содержать только целочисленные значения")


def get_optimal_row_idx(matrix: [[int]]) -> int:
    """Вспомогательная функция для поиска оптимальной строки матрицы с наибольшим
    количеством нулей

    :param matrix: целочисленная квадратная матрица
    :return: индекс оптимальной строки
    """

    zero_count = row_idx = 0
    for idx, row in enumerate(matrix):  # обход элементов строки матрицы
        current_row_zero_count = row.count(0)
        if current_row_zero_count > zero_count:  # если найдена строка с большим количеством нулей
            zero_count = current_row_zero_count
            row_idx = idx
    return row_idx



def main():
    matrix = [[1, 2],
              [3, 4]]
    print('Матрица')
    for row in matrix:
        print(row)

    print(f'Определитель матрицы равен {calculate_determinant(matrix)}')


if __name__ == '__main__':
    main()

