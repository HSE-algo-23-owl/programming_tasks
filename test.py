import unittest

from main import fibonacci_rec, fibonacci_iter, rabbits

MONTH = 'month'
LIFETIME = 'lifetime'
RABBITS = 'rabbits'
IS_RABBIT_IMPLEMENTED = bool(rabbits(1, 2))


class TestFibonacci(unittest.TestCase):
    """Тесты для проверки функций вычисления числа Фибоначчи"""
    fibonacci_numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377,
                         610, 987, 1597, 2584, 4181, 6765, 10946, 17711]

    def test_fibonacci_rec(self):
        """Проверка работы рекурсивной функции вычисления числа Фибоначчи"""
        for index, number in enumerate(self.fibonacci_numbers):
            self.assertEqual(fibonacci_rec(index + 1), number)

    def test_fibonacci_iter(self):
        """Проверка работы итеративной функции вычисления числа Фибоначчи"""
        for index, number in enumerate(self.fibonacci_numbers):
            self.assertEqual(fibonacci_iter(index + 1), number)

    @unittest.skipIf(not IS_RABBIT_IMPLEMENTED,
                     'Тест не выполняется если функция rabbits не реализована')
    def test_rabbits(self):
        """Проверка работы функции расчета количества пар кроликов с
        установленной продолжительностью жизни"""
        test_data = [{MONTH: 1, LIFETIME: 2, RABBITS: 1},
                     {MONTH: 2, LIFETIME: 2, RABBITS: 1},
                     {MONTH: 3, LIFETIME: 7, RABBITS: 2},
                     {MONTH: 3, LIFETIME: 8, RABBITS: 2},
                     {MONTH: 4, LIFETIME: 8, RABBITS: 3},
                     {MONTH: 5, LIFETIME: 6, RABBITS: 5},
                     {MONTH: 6, LIFETIME: 8, RABBITS: 8},
                     {MONTH: 7, LIFETIME: 9, RABBITS: 13},
                     {MONTH: 8, LIFETIME: 7, RABBITS: 20},
                     {MONTH: 9, LIFETIME: 9, RABBITS: 34}]
        for data in test_data:
            self.assertEqual(data[RABBITS],
                             rabbits(data[MONTH], data[LIFETIME]))


if __name__ == '__main__':
    unittest.main()
