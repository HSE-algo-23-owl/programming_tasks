import unittest
from main import floydWarshall, PARAM_ERR_MSG, INF


class Test(unittest.TestCase):
    """Это будет класс для тестирования разработанного алгоритма"""

    def test_incorrect_matrix(self):
        """Проверяет выброс исключения при передаче некорректного значения
        матрицы."""
        incorrect_values = [None, [], [[]], (), {}, 'str', 1, 1.1]
        for value in incorrect_values:
            self.assertRaisesRegex(TypeError, PARAM_ERR_MSG,
                                   floydWarshall, value)

    def test_not_square_rectangle(self):
        """Проверяет выброс исключения при передаче не квадратной матрицы."""
        matrix = [[3, 3, 5],
                  [3, 2, 4]]
        self.assertRaisesRegex(TypeError, PARAM_ERR_MSG,
                               floydWarshall, matrix)

    def test_not_square_jag(self):
        """Проверяет выброс исключения при передаче рваной матрицы."""
        matrix = [[3, 3, 5],
                  [3, 2],
                  [2, 5, 7]]
        self.assertRaisesRegex(TypeError, PARAM_ERR_MSG,
                               floydWarshall, matrix)

    def test_has_not_number(self):
        """Проверяет выброс исключения при наличии в матрице нецелочисленного
        значения."""
        matrix = [['str', 3],
                  [3, 2]]
        self.assertRaisesRegex(TypeError, PARAM_ERR_MSG,
                               floydWarshall, matrix)

    def test_has_not_negative_cycle(self):
        """Проверяет верно ли алгоритм определят отсутствие цикла отрицательной длины в графе"""
        matrix = [[0, 5, INF, 10],
                  [INF, 0, 3, INF],
                  [INF, INF, 0, 1],
                  [INF, INF, INF, 0]
                  ]
        self.assertFalse(floydWarshall(matrix)[1])

    def test_has_negative_cycle(self):
        """Проверяет верно ли алгоритм определят присутствие цикла отрицательной длины в графе"""
        matrix = [[0, 5, INF, 10],
                  [-3, 0, 3, INF],
                  [INF, -10, 0, 1],
                  [INF, INF, INF, 0]
                  ]
        self.assertTrue(floydWarshall(matrix)[1])

    def test_right_answer(self):
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


if __name__ == '__main__':
    unittest.main()
