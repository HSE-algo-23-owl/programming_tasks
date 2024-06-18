import unittest
from main import floydWarshall, PARAM_ERR_MSG, INF


class Test(unittest.TestCase):
    """Это будет класс для тестирования разработанного алгоритма"""

    def test_incorrect_matrix(self):  # 1
        """Проверяет выброс исключения при передаче некорректного значения
        матрицы."""
        incorrect_values = [None, [], [[]], (), {}, 'str', 1, 1.1]
        for value in incorrect_values:
            self.assertRaisesRegex(TypeError, PARAM_ERR_MSG,
                                   floydWarshall, value)

    def test_not_square_rectangle(self):  # 2
        """Проверяет выброс исключения при передаче не квадратной матрицы."""
        matrix = [[3, 3, 5],
                  [3, 2, 4]]
        self.assertRaisesRegex(TypeError, PARAM_ERR_MSG,
                               floydWarshall, matrix)

    def test_not_square_jag(self):  # 3
        """Проверяет выброс исключения при передаче рваной матрицы."""
        matrix = [[3, 3, 5],
                  [3, 2],
                  [2, 5, 7]]
        self.assertRaisesRegex(TypeError, PARAM_ERR_MSG,
                               floydWarshall, matrix)

    def test_has_not_number(self):  # 4
        """Проверяет выброс исключения при наличии в матрице нецелочисленного
        значения."""
        matrix = [['str', 3],
                  [3, 2]]
        self.assertRaisesRegex(TypeError, PARAM_ERR_MSG,
                               floydWarshall, matrix)

    def test_has_not_negative_cycle(self):  # 5
        """Проверяет верно ли алгоритм определят отсутствие цикла отрицательной длины в графе"""
        matrix = [[0, 5, INF, 10],
                  [INF, 0, 3, INF],
                  [INF, INF, 0, 1],
                  [INF, INF, INF, 0]
                  ]
        self.assertFalse(floydWarshall(matrix)[1])

    def test_has_negative_cycle(self):  # 6
        """Проверяет верно ли алгоритм определят присутствие цикла отрицательной длины в графе"""
        matrix = [[0, 5, INF, 10],
                  [-3, 0, 3, INF],
                  [INF, -10, 0, 1],
                  [INF, INF, INF, 0]
                  ]
        self.assertTrue(floydWarshall(matrix)[1])

    def test_right_answer(self):  # 7
        """Проверяет верно ли, работает алгоритм на 4 вершинах"""
        matrix = [[0, 5, INF, 10],
                  [INF, 0, 3, INF],
                  [INF, INF, 0, 1],
                  [INF, INF, INF, 0]
                  ]
        right_matrix = [[0, 5, 8, 9],
                        [INF, 0, 3, 4],
                        [INF, INF, 0, 1],
                        [INF, INF, INF, 0]]
        result = floydWarshall(matrix)[0]
        self.assertEqual(result, right_matrix)

    def test_one_matrix(self):  # 8
        """Проверяет работу алгоритма на единичной матрице"""
        matrix = [[1]]
        result = floydWarshall(matrix)
        self.assertEqual(result[0], [[1]])
        self.assertFalse(result[1])

    def test_big_matrix(self):  # 9
        """Проверяет работу алгоритма на матрице из 12 вершин без отрицательного цикла"""
        right_matrix = [[0, 2, 5, 6, 8, 11, 15, 20, 26, 33, 34, 36],
                        [2, 0, 3, 4, 6, 9, 13, 18, 24, 31, 32, 34],
                        [5, 3, 0, 1, 3, 6, 10, 15, 21, 28, 29, 31],
                        [6, 4, 1, 0, 2, 5, 9, 14, 20, 27, 28, 30],
                        [8, 6, 3, 2, 0, 3, 7, 12, 18, 25, 26, 28],
                        [11, 9, 6, 5, 3, 0, 4, 9, 15, 22, 23, 25],
                        [15, 13, 10, 9, 7, 4, 0, 5, 11, 18, 19, 21],
                        [20, 18, 15, 14, 12, 9, 5, 0, 6, 13, 14, 16],
                        [26, 24, 21, 20, 18, 15, 11, 6, 0, 7, 8, 10],
                        [33, 31, 28, 27, 25, 22, 18, 13, 7, 0, 1, 3],
                        [34, 32, 29, 28, 26, 23, 19, 14, 8, 1, 0, 2],
                        [36, 34, 31, 30, 28, 25, 21, 16, 10, 3, 2, 0]]
        matrix = [[0, 2, INF, INF, INF, INF, INF, INF, INF, INF, INF, INF],
                  [2, 0, 3, INF, INF, INF, INF, INF, INF, INF, INF, INF],
                  [INF, 3, 0, 1, INF, INF, INF, INF, INF, INF, INF, INF],
                  [INF, INF, 1, 0, 2, INF, INF, INF, INF, INF, INF, INF],
                  [INF, INF, INF, 2, 0, 3, INF, INF, INF, INF, INF, INF],
                  [INF, INF, INF, INF, 3, 0, 4, INF, INF, INF, INF, INF],
                  [INF, INF, INF, INF, INF, 4, 0, 5, INF, INF, INF, INF],
                  [INF, INF, INF, INF, INF, INF, 5, 0, 6, INF, INF, INF],
                  [INF, INF, INF, INF, INF, INF, INF, 6, 0, 7, INF, INF],
                  [INF, INF, INF, INF, INF, INF, INF, INF, 7, 0, 1, INF],
                  [INF, INF, INF, INF, INF, INF, INF, INF, INF, 1, 0, 2],
                  [INF, INF, INF, INF, INF, INF, INF, INF, INF, INF, 2, 0]]
        result = floydWarshall(matrix)
        self.assertEqual(right_matrix, result[0])
        self.assertFalse(result[1])

    def test_big_matrix_w_negative_cycle(self):  # 10
        """Проверяет работу алгоритма на матрице из 12 вершин с отрицательным циклом """
        right_matrix = [[0, 1, 4, 5, 7, 10, 14, 19, 25, 32, 33, 35],
                        [1, -1, 2, 3, 5, 8, 12, 17, 23, 30, 31, 33],
                        [-2, -4, -1, 0, 2, 5, 9, 14, 20, 27, 28, 30],
                        [-3, -5, -2, -1, 1, 4, 8, 13, 19, 26, 27, 29],
                        [-5, -7, -4, -3, -1, 2, 6, 11, 17, 24, 25, 27],
                        [-9, -11, -8, -7, -5, -2, 2, 7, 13, 20, 21, 23],
                        [-5, -7, -4, -3, -1, 2, 0, 5, 11, 18, 19, 21],
                        [0, -2, 1, 2, 4, 7, 5, 0, 6, 13, 14, 16],
                        [6, 4, 7, 8, 10, 13, 11, 6, 0, 7, 8, 10],
                        [13, 11, 14, 15, 17, 20, 18, 13, 7, 0, 1, 3],
                        [14, 12, 15, 16, 18, 21, 19, 14, 8, 1, 0, 2],
                        [16, 14, 17, 18, 20, 23, 21, 16, 10, 3, 2, 0]]
        matrix = [[0, 2, INF, INF, INF, INF, INF, INF, INF, INF, INF, INF],
                  [2, 0, 3, INF, INF, INF, INF, INF, INF, INF, INF, INF],
                  [INF, 3, 0, 1, INF, INF, INF, INF, INF, INF, INF, INF],
                  [INF, INF, 1, 0, 2, INF, INF, INF, INF, INF, INF, INF],
                  [INF, INF, INF, 2, 0, 3, INF, INF, INF, INF, INF, INF],
                  [INF, -10, INF, INF, 3, 0, 4, INF, INF, INF, INF, INF],
                  [INF, INF, INF, INF, INF, 4, 0, 5, INF, INF, INF, INF],
                  [INF, INF, INF, INF, INF, INF, 5, 0, 6, INF, INF, INF],
                  [INF, INF, INF, INF, INF, INF, INF, 6, 0, 7, INF, INF],
                  [INF, INF, INF, INF, INF, INF, INF, INF, 7, 0, 1, INF],
                  [INF, INF, INF, INF, INF, INF, INF, INF, INF, 1, 0, 2],
                  [INF, INF, INF, INF, INF, INF, INF, INF, INF, INF, 2, 0]]
        result = floydWarshall(matrix)
        self.assertEqual(result[0], right_matrix)
        self.assertTrue(result[1])


if __name__ == '__main__':
    unittest.main()
