import unittest

from main import get_triangle_path_count, binomial_coefficient, \
    PATH_LENGTH_ERROR_MSG, NOT_INT_VALUE_TEMPL, NEGATIVE_VALUE_TEMPL, \
    N_LESS_THAN_K_ERROR_MSG


class TestTrianglePath(unittest.TestCase):
    __incorrect_length_values = [None, 0, -1, 1.1, True, 'string']
    """Метод для проверки количества маршрутов с использованием общей формулы"""
    @staticmethod
    def __calculate_result(length):
        return 1/3 * 2**length + 2/3 * (-1)**length

    def test_incorrect_length_values(self):
        """Проверяет выброс исключения при некорректном значении параметра
        длина маршрута"""
        for incorrect_val in self.__incorrect_length_values:
            self.assertRaisesRegex(ValueError, PATH_LENGTH_ERROR_MSG,
                                   get_triangle_path_count, incorrect_val)

    def test_triangle_path(self):
        """Проверяет корректность вычисления количества маршрутов длиной
        от 1 до 10"""
        for i in range(1, 10):
            self.assertEqual(get_triangle_path_count(i),
                             TestTrianglePath.__calculate_result(i))


class TestBinomialCoefficient(unittest.TestCase):
    def test_n_less_than_k(self):
        """Проверяет выброс исключения при значении параметра n меньше чем k"""
        self.assertRaisesRegex(ValueError, N_LESS_THAN_K_ERROR_MSG,
                               binomial_coefficient, 1, 2)

    def test_negative_n(self):
        """Проверяет выброс исключения при отрицательном значении параметра n"""
        self.assertRaisesRegex(ValueError, NEGATIVE_VALUE_TEMPL.format('n'),
                               binomial_coefficient, -2, 2)

    def test_negative_k(self):
        """Проверяет выброс исключения при отрицательном значении параметра k"""
        self.assertRaisesRegex(ValueError, NEGATIVE_VALUE_TEMPL.format('k'),
                               binomial_coefficient, 2, -2)

    def test_n_is_not_int(self):
        """Проверяет выброс исключения при нечисловом значении параметра n"""
        self.assertRaisesRegex(ValueError, NOT_INT_VALUE_TEMPL.format('n'),
                               binomial_coefficient, 'a', 2)

    def test_k_is_not_int(self):
        """Проверяет выброс исключения при нечисловом значении параметра k"""
        self.assertRaisesRegex(ValueError, NOT_INT_VALUE_TEMPL.format('k'),
                               binomial_coefficient, 2, 'b')

    def test_binomial_coefficient_tiny(self):
        """Проверка вычисления биномиального коэффициента при небольших
        значениях параметров"""
        pascals_triangle = [[1],
                            [1, 1],
                            [1, 2, 1],
                            [1, 3, 3, 1],
                            [1, 4, 6, 4, 1]]
        for n in range(len(pascals_triangle)):
            for k in range(len(pascals_triangle[n])):
                for use_rec in [True, False]:
                    res = binomial_coefficient(n, k, use_rec=use_rec)
                    self.assertEqual(res, pascals_triangle[n][k])

    def test_binomial_coefficient_middle(self):
        """Проверка вычисления биномиального коэффициента при средних
        значениях параметров"""
        for use_rec in [True, False]:
            res = binomial_coefficient(10, 5, use_rec=use_rec)
            self.assertEqual(res, 252)

    def test_binomial_coefficient_large(self):
        """Проверка вычисления биномиального коэффициента при больших
        значениях параметров"""
        for use_rec in [True, False]:
            res = binomial_coefficient(30, 20, use_rec=use_rec)
            self.assertEqual(res, 30045015)


if __name__ == '__main__':
    unittest.main()
