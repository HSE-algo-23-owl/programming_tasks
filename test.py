import unittest

from main import get_min_cost_path, COST, PATH, PARAM_ERR_MSG


class TestTablePath(unittest.TestCase):
    def test_none(self):
        """Проверяет выброс исключения при передаче None в качестве параметра"""
        self.assertRaisesRegex(ValueError, PARAM_ERR_MSG, get_min_cost_path,
                               None)

    def test_empty(self):
        """Проверяет выброс исключения при передаче пустого списка в
        качестве параметра"""
        self.assertRaisesRegex(ValueError, PARAM_ERR_MSG, get_min_cost_path, [])

    def test_empty_row(self):
        """Проверяет выброс исключения при передаче списка с пустым списком в
        качестве параметра"""
        self.assertRaisesRegex(ValueError, PARAM_ERR_MSG, get_min_cost_path,
                               [[]])

    def test_str_value(self):
        """Проверяет выброс исключения при наличии в матрице нечислового
        значения"""
        self.assertRaisesRegex(ValueError, PARAM_ERR_MSG, get_min_cost_path,
                               [[1, 'ab']])

    def test_jag(self):
        """Проверяет выброс исключения при наличии в матрице строк разной
        длины"""
        table = [[1., 2., 3.],
                 [1., 2.]]
        self.assertRaisesRegex(ValueError, PARAM_ERR_MSG, get_min_cost_path,
                               table)

    def test_single(self):
        """Проверяет поиск кратчайшего пути в матрице размером 1*1"""
        self.assertEqual(get_min_cost_path([[1]]),
                         {COST: 1., PATH: [(0, 0)]})

    def test_single_none(self):
        """Проверяет поиск кратчайшего пути в матрице размером 1*1 с ячейкой,
        запрещенной к посещению"""
        self.assertEqual(get_min_cost_path([[None]]),
                         {COST: None, PATH: None})

    def test_double(self):
        """Проверяет поиск кратчайшего пути в матрице размером 2*2"""
        table = [[1.1, 2],
                 [3, 4]]
        self.assertEqual(get_min_cost_path(table),
                         {COST: 7.1, PATH: [(0, 0), (0, 1), (1, 1)]})

    def test_double_with_none(self):
        """Проверяет поиск кратчайшего пути в матрице размером 2*2 с ячейкой,
        запрещенной к посещению"""
        table = [[1.1, None],
                 [3, 4]]
        self.assertEqual(get_min_cost_path(table),
                         {COST: 8.1, PATH: [(0, 0), (1, 0), (1, 1)]})

    def test_negative(self):
        """Проверяет поиск кратчайшего пути при наличии в матрице
        отрицательного значения"""
        table = [[1.1, 2],
                 [-3, 4]]
        self.assertEqual(get_min_cost_path(table),
                         {COST: 2.1, PATH: [(0, 0), (1, 0), (1, 1)]})

    def test_triple(self):
        """Проверяет поиск кратчайшего пути в матрице размером 3*3"""
        table = [[1, 2, 2],
                 [3, 4, 2],
                 [1, 1, 2]]
        self.assertEqual(get_min_cost_path(table),
                         {COST: 8.,
                          PATH: [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]})

    def test_triple_no_path(self):
        """Проверяет поиск кратчайшего пути в матрице размером 3*3,
        пути не существует"""
        table = [[1, None, 2],
                 [None, 4, 2],
                 [1, 1, 2]]
        self.assertEqual(get_min_cost_path(table),
                         {COST: None, PATH: None})

    def test_rectangle(self):
        """Проверяет поиск кратчайшего пути в прямоугольной матрице
        размером 2*3"""
        table = [[1, 2, 2],
                 [3, 4, 1]]
        self.assertEqual(get_min_cost_path(table),
                         {COST: 6.,
                          PATH: [(0, 0), (0, 1), (0, 2), (1, 2)]})

    def test_rectangle_with_none(self):
        """Проверяет поиск кратчайшего пути в прямоугольной матрице
        размером 2*3 с ячейкой, запрещенной к посещению"""
        table = [[1, None, None],
                 [3, 4, 1]]
        self.assertEqual(get_min_cost_path(table),
                         {COST: 9.,
                          PATH: [(0, 0), (1, 0), (1, 1), (1, 2)]})

    def test_square(self):
        """Проверяет поиск кратчайшего пути в квадратной матрице размером 6*6"""
        table = [[1, 2, 2, 1, 3, 4],
                 [3, 1, 1, 5, 7, 6],
                 [3, 4, 1, 2, 7, 6],
                 [5, 7, 1, 6, 4, 4],
                 [5, 9, 2, 3, 5, 8],
                 [2, 2, 1, 3, 1, 6]]
        self.assertEqual(get_min_cost_path(table),
                         {COST: 20., PATH: [(0, 0), (0, 1), (1, 1),
                                            (1, 2), (2, 2), (3, 2), (4, 2),
                                            (5, 2), (5, 3), (5, 4), (5, 5)]})

    def test_square_with_none(self):
        """Проверяет поиск кратчайшего пути в квадратной матрице размером 6*6
         с ячейкой, запрещенной к посещению"""
        table = [[1, 2, 2, 1, 3, None],
                 [3, 1, 1, 5, None, 6],
                 [3, 4, 1, 2, 7, 6],
                 [5, 7, None, 6, 4, 4],
                 [5, None, 2, 3, 5, 8],
                 [None, 2, 1, 3, 1, 6]]
        self.assertEqual(get_min_cost_path(table),
                         {COST: 27., PATH: [(0, 0), (0, 1), (1, 1),
                                            (1, 2), (2, 2), (2, 3), (3, 3),
                                            (4, 3), (5, 3), (5, 4), (5, 5)]})

    def test_rectangle_large(self):
        """Проверяет поиск кратчайшего пути в прямоугольной матрице
        размером 12*6"""
        table = [[8, 9, 2, 1, 6, 9],
                 [2, 3, 4, 8, 5, 1],
                 [4, 1, 7, 7, 1, 7],
                 [5, 6, 2, 8, 5, 6],
                 [3, 5, 2, 5, 8, 3],
                 [6, 9, 1, 3, 1, 5],
                 [7, 5, 4, 4, 2, 9],
                 [8, 7, 4, 1, 3, 5],
                 [6, 5, 7, 7, 6, 2],
                 [6, 2, 4, 8, 6, 3],
                 [7, 7, 2, 4, 5, 7],
                 [3, 8, 1, 6, 7, 1]]
        self.assertEqual(get_min_cost_path(table),
                         {COST: 52., PATH: [(0, 0), (1, 0), (1, 1),
                                            (2, 1), (3, 1), (3, 2), (4, 2),
                                            (5, 2), (5, 3), (5, 4), (6, 4),
                                            (7, 4), (7, 5), (8, 5), (9, 5),
                                            (10, 5), (11, 5)]})

    def test_rectangle_large_with_none(self):
        """Проверяет поиск кратчайшего пути в прямоугольной матрице
        размером 12*6 с ячейкой, запрещенной к посещению"""
        table = [[8, 9, 2, 1, 6, None],
                 [2, 3, 4, 8, 5, 1],
                 [4, 1, 7, 7, 1, 7],
                 [5, 6, 2, 8, 5, 6],
                 [3, 5, 2, 5, 8, 3],
                 [6, 9, 1, 3, 1, 5],
                 [7, 5, 4, 4, 2, 9],
                 [8, 7, 4, 1, 3, 5],
                 [6, 5, 7, 7, 6, 2],
                 [6, 2, 4, 8, 6, 3],
                 [7, 7, 2, 4, 5, None],
                 [3, 8, 1, 6, 7, 1]]
        self.assertEqual(get_min_cost_path(table),
                         {COST: 59.,
                          PATH: [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1),
                                 (3, 2), (4, 2), (5, 2), (5, 3), (5, 4),
                                 (6, 4), (7, 4), (8, 4), (9, 4), (10, 4),
                                 (11, 4), (11, 5)]})


if __name__ == '__main__':
    unittest.main()
