def get_minor(matrix, ind):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    result = 0
    for i in range(len(matrix[0])):
        matrix_for_i = delete_rows(matrix, i)
        if i % 2 == 0:
            result += (matrix[0][i] * get_minor(matrix_for_i, i))
        else:
            result += (matrix[0][i] * (-1 * get_minor(matrix_for_i, i)))
    return result


def delete_rows(matrix, ind):
    new_matrix = []
    for row in matrix[1::]:
        new_row = []
        for elem in range(len(row)):
            if elem != ind:
                new_row.append(row[elem])
        new_matrix.append(new_row)
    return new_matrix


def calculate_determinant(matrix):
    check_matrix_raises_ex(matrix)
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    result = 0
    for i in range(len(matrix[0])):
        matrix_for_i = delete_rows(matrix, i)
        if i % 2 == 0:
            result += (matrix[0][i] * get_minor(matrix_for_i, i))
        else:
            result += (matrix[0][i] * (-1 * get_minor(matrix_for_i, i)))
    return result


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
