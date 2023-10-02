import copy


def calculate_determinant(matrix):
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    matrix_exception(matrix)
    if len(matrix)==1:
        return matrix[0][0]
    else:
        return minor_matrix(matrix)



def matrix_exception(matrix):
    if type(matrix)!= list or matrix==[]:
        raise Exception('Не матрица')
    a = len(matrix)
    for b in matrix:
        if len(b)!= a:
            raise Exception('Не квадратная матрица')
    for b in matrix:
        for i in b:
            if type(i) != int:
                raise Exception('Не целочисленная матрица')
def minor_matrix(matrix):
    if len(matrix)==2:
        return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    res = 0
    if len(matrix)>2:
        for b in range(len(matrix)):#столбец
            temp_matrix = copy.deepcopy(matrix)
            print (temp_matrix)
            for delete in range(len(matrix)):#сторка
                del temp_matrix[delete][b]
            del temp_matrix[0]
            if (b+2) % 2 == 0:
                res += (matrix[0][b] * minor_matrix(temp_matrix))
            else:
                res += (matrix[0][b] * (-1 * minor_matrix(temp_matrix)))
    return res

def main():
    matrix = [[1, 2],
              [3, 4]]
    print('Матрица')
    for row in matrix:
        print(row)

    print(f'Определитель матрицы равен {calculate_determinant(matrix)}')


if __name__ == '__main__':
    main()
