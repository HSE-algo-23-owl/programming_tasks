import unittest
import numpy as np


from main import get_random_matrix_and_det, MATRIX, DET


class TestMatrixGenerator(unittest.TestCase):
    """Набор тестов для проверки генератора матриц"""
    def test_none(self):
        """Проверка выброса исключения при передаче в параметр None"""
        self.assertRaises(Exception, 'Порядок матрицы не является целым числом',
                          get_random_matrix_and_det, None)

    def test_float(self):
        """Проверка выброса исключения при передаче в параметр
        вещественного числа"""
        self.assertRaises(Exception, 'Порядок матрицы не является целым числом',
                          get_random_matrix_and_det, 1.1)

    def test_zero(self):
        """Проверка выброса исключения при передаче в параметр нуля"""
        self.assertRaises(Exception, 'Порядок матрицы меньше 1',
                          get_random_matrix_and_det, 0)

    def test_neg(self):
        """Проверка выброса исключения при передаче в параметр
        отрицательного значения"""
        self.assertRaises(Exception, 'Порядок матрицы меньше 1',
                          get_random_matrix_and_det, -1)

    def test_det_with_numpy(self):
        """Проверка генератора на порядках 1-9. Проверяется порядок матрицы
        и расчет определителя"""
        for order in range(1, 10):
            gen_result = get_random_matrix_and_det(order)
            matrix = gen_result[MATRIX]

            self.assertEqual(order, len(matrix))
            for row in matrix:
                self.assertEqual(order, len(row))

            self.assertEqual(round(np.linalg.det(np.array(matrix))),
                             gen_result[DET])


if __name__ == '__main__':
    unittest.main()
