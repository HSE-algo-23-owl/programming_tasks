import unittest

from main import get_path_count, PARAM_ERR_MSG


class TestTablePath(unittest.TestCase):
    def test_none(self):
        """Проверяет выброс исключения при передаче None в качестве параметра"""
        self.assertRaisesRegex(ValueError, PARAM_ERR_MSG, get_path_count,
                               None)

    def test_empty(self):
        """Проверяет выброс исключения при передаче пустого списка в
        качестве параметра"""
        self.assertRaisesRegex(ValueError, PARAM_ERR_MSG, get_path_count, [])

    def test_empty_row(self):
        """Проверяет выброс исключения при передаче списка с пустым списком в
        качестве параметра"""
        self.assertRaisesRegex(ValueError, PARAM_ERR_MSG, get_path_count,
                               [[]])

    def test_incorrect_values(self):
        """Проверяет выброс исключения при наличии в матрице недопустимого
        значения"""
        incorrect_values = [-1, 1.1, 2, None, 'str', []]
        for value in incorrect_values:
            self.assertRaisesRegex(ValueError, PARAM_ERR_MSG,
                                   get_path_count, [[1, value]])

    def test_jag(self):
        """Проверяет выброс исключения при наличии в матрице строк разной
        длины"""
        table = [[1, 0, 1],
                 [1, 1]]
        self.assertRaisesRegex(ValueError, PARAM_ERR_MSG, get_path_count,
                               table)

    def test_single(self):
        """Проверяет поиск количества путей в матрице размером 1*1"""
        self.assertEqual(get_path_count([[1]]), 1)

    def test_single_none(self):
        """Проверяет поиск количества путей в матрице размером 1*1 с ячейкой,
        запрещенной к посещению"""
        self.assertEqual(get_path_count([[0]]), 0)

    def test_double(self):
        """Проверяет поиск количества путей в матрице размером 2*2"""
        table = [[1, 1],
                 [1, 1]]
        self.assertEqual(get_path_count(table), 2)

    def test_double_with_none(self):
        """Проверяет поиск количества путей в матрице размером 2*2 с ячейкой,
        запрещенной к посещению"""
        table = [[1, 0],
                 [1, 1]]
        self.assertEqual(get_path_count(table), 1)

    def test_triple(self):
        """Проверяет поиск количества путей в матрице размером 3*3"""
        table = [[1, 1, 1],
                 [1, 1, 1],
                 [1, 1, 1]]
        self.assertEqual(get_path_count(table), 6)

    def test_triple_no_path(self):
        """Проверяет поиск количества путей в матрице размером 3*3,
        пути не существует"""
        table = [[1, 0, 1],
                 [0, 1, 1],
                 [1, 1, 1]]
        self.assertEqual(get_path_count(table), 0)

    def test_rectangle(self):
        """Проверяет поиск количества путей в прямоугольной матрице
        размером 2*3"""
        table = [[1, 1, 1],
                 [1, 1, 1]]
        self.assertEqual(get_path_count(table), 3)

    def test_rectangle_with_none(self):
        """Проверяет поиск количества путей в прямоугольной матрице
        размером 2*3 с ячейкой, запрещенной к посещению"""
        table = [[1, 0, 0],
                 [1, 1, 1]]
        self.assertEqual(get_path_count(table), 1)

    def test_square(self):
        """Проверяет поиск количества путей в квадратной матрице размером 6*6"""
        table = [[1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1]]
        self.assertEqual(get_path_count(table), 252)

    def test_square_with_none(self):
        """Проверяет поиск количества путей в квадратной матрице размером 6*6
         с ячейками, запрещенными к посещению"""
        table = [[1, 1, 1, 1, 1, 0],
                 [1, 1, 1, 1, 0, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 0, 1, 1, 1],
                 [1, 0, 1, 1, 1, 1],
                 [0, 1, 1, 1, 1, 1]]
        self.assertEqual(get_path_count(table), 100)

    def test_rectangle_large(self):
        """Проверяет поиск количества путей в прямоугольной матрице
        размером 12*6"""
        table = [[1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1]]
        self.assertEqual(get_path_count(table), 4368)

    def test_rectangle_large_with_none(self):
        """Проверяет поиск количества путей в прямоугольной матрице
        размером 12*6 с ячейками, запрещенными к посещению"""
        table = [[1, 1, 1, 1, 1, 1],
                 [1, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 1]]
        self.assertEqual(get_path_count(table), 2)


if __name__ == '__main__':
    unittest.main()
