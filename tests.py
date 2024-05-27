import unittest
import random

from main import get_salesman_path, DISTANCE, PATH, NullableNumber, \
    PARAM_ERR_MSG, NEG_VALUE_ERR_MSG, MAX_VERTEXES_ERR_MSG


class TestSalesManPath(unittest.TestCase):
    @staticmethod
    def __check_path(matrix: list[list[NullableNumber]],
                     result: dict[str, float | list[int]]) -> bool:
        """Проверяет корректность найденного пути."""
        distance = result[DISTANCE]
        path = result[PATH]
        if len(matrix) + 1 != len(path):
            return False
        if len(matrix) == 1 and path != [0]:
            return False
        if path[0] != path[-1]:
            return False
        if set(path) != set([n for n in range(len(matrix))]):
            return False
        summ = 0
        for i in range(1, len(path)):
            src = path[i - 1]
            trg = path[i]
            summ += matrix[src][trg]
        if summ != distance:
            return False
        return True

    def test_incorrect_matrix(self):
        """Проверяет выброс исключения при передаче некорректного значения
        матрицы."""
        incorrect_values = [None, [], [[]], (), {}, 'str', 1, 1.1]
        for value in incorrect_values:
            self.assertRaisesRegex(TypeError, PARAM_ERR_MSG,
                                   get_salesman_path, value)

    def test_not_square_rectangle(self):
        """Проверяет выброс исключения при передаче не прямоугольной матрицы."""
        matrix = [[3., 3., 5.],
                  [3., 2., 4.]]
        self.assertRaisesRegex(TypeError, PARAM_ERR_MSG,
                               get_salesman_path, matrix)

    def test_not_square_jag(self):
        """Проверяет выброс исключения при передаче рваной матрицы."""
        matrix = [[3., 3., 5.],
                  [3., 2.],
                  [2., 5., 7.]]
        self.assertRaisesRegex(TypeError, PARAM_ERR_MSG,
                               get_salesman_path, matrix)

    def test_has_not_number(self):
        """Проверяет выброс исключения при наличии в матрице нечислового
        значения."""
        matrix = [['str', 3.],
                  [3., 2.]]
        self.assertRaisesRegex(TypeError, PARAM_ERR_MSG,
                               get_salesman_path, matrix)

    def test_has_negative_number(self):
        """Проверяет выброс исключения при наличии в матрице отрицательного
        значения."""
        matrix = [[1, 3.],
                  [3., -0.1]]
        self.assertRaisesRegex(ValueError, NEG_VALUE_ERR_MSG,
                               get_salesman_path, matrix)

    def test_single(self):
        """Проверяет построение маршрута в матрице единичного порядка."""
        matrix = [[None]]
        self.assertEqual(get_salesman_path(matrix),
                         {DISTANCE: 0, PATH: [0]})

    def test_double(self):
        """Проверяет построение маршрута в матрице второго порядка."""
        matrix = [[None, 1.],
                  [2., None]]
        self.assertEqual(get_salesman_path(matrix),
                         {DISTANCE: 3, PATH: [0, 1, 0]})

    def test_has_not_path(self):
        """Проверяет вывод данных при отсутствии маршрута в матрице."""
        matrix = [[None, 1.],
                  [None, None]]
        self.assertEqual(get_salesman_path(matrix),
                         {DISTANCE: None, PATH: []})

    def test_triple(self):
        """Проверяет построение маршрута в матрице третьего порядка."""
        matrix = [[None, 1., 2.],
                  [4., None, 3.],
                  [None, 5., 6.]]
        result = get_salesman_path(matrix)
        self.assertEqual(result[DISTANCE], 11.)
        self.assertTrue(self.__check_path(matrix, result))

    def test_four(self):
        """Проверяет построение маршрута в матрице четвертого порядка."""
        matrix = [[1., 2., 3., 4.],
                  [5., 6., 7., 8.],
                  [9., 10., 11., 12.],
                  [13., 14., 15., 16.]]
        result = get_salesman_path(matrix)
        self.assertEqual(result[DISTANCE], 34.)
        self.assertTrue(self.__check_path(matrix, result))

    def test_pentad(self):
        """Проверяет построение маршрута в матрице пятого порядка."""
        matrix = [[None, 12., 9., 9., 12.],
                  [9., None, 8., 19., 15.],
                  [7., 1., None, 17., 11.],
                  [5., 9., 12., None, 16.],
                  [14., 6., 12., 22., None]]
        result = get_salesman_path(matrix)
        self.assertEqual(result[DISTANCE], 46.)
        self.assertTrue(self.__check_path(matrix, result))

    def test_random_simple(self):
        """Проверяет построение маршрута в простой случайной матрице."""
        order = random.randint(3, 9)
        value = float(random.randint(1, 100))
        matrix = [[value for _ in range(order)] for _ in range(order)]
        result = get_salesman_path(matrix)
        self.assertEqual(result[DISTANCE], order*value)
        self.assertTrue(self.__check_path(matrix, result))

    def test_random(self):
        """Проверяет построение маршрута в случайной матрице."""
        order = random.randint(3, 9)
        path = [n for n in range(1, order)]
        random.shuffle(path)
        path = [0] + path + [0]
        value = 1.
        distance = 0
        matrix = [[None for _ in range(order)] for _ in range(order)]
        for i in range(1, len(path)):
            src = path[i - 1]
            trg = path[i]
            matrix[src][trg] = value
            distance += value
            value += 1.
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] is None:
                    matrix[i][j] = value + float(random.randint(1, 100))
        result = get_salesman_path(matrix)

        self.assertEqual(result[DISTANCE], distance)
        self.assertTrue(self.__check_path(matrix, result))

    def test_exceeding_vertex_limit(self):
        matrix = [[None] * 16 for _ in range(16)]
        with self.assertRaises(ValueError) as cm:
            get_salesman_path(matrix)
        self.assertEqual(str(cm.exception), MAX_VERTEXES_ERR_MSG)
if __name__ == '__main__':
    unittest.main()
