import unittest

from knapsack_problem.brute_force import brute_force
from knapsack_problem.constants import COST
from test import check_knapsack_items


class TestBruteForce(unittest.TestCase):
    """Набор тестов для проверки решения задачи о рюкзаке методом полного
    перебора."""

    def test_2(self):
        """Проверка решения задачи о рюкзаке для двух предметов."""
        weights = [1, 1]
        costs = [1, 2]
        weight_limit = 1
        result = brute_force(weights, costs, weight_limit)
        self.assertEqual(result[COST], 2)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit,
                                             result))

    def test_3(self):
        """Проверка решения задачи о рюкзаке для трех предметов."""
        weights = [1, 1, 2]
        costs = [1, 2, 2]
        weight_limit = 2
        result = brute_force(weights, costs, weight_limit)
        self.assertEqual(result[COST], 3)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit,
                                             result))

    def test_4(self):
        """Проверка решения задачи о рюкзаке для четырех предметов."""
        weights = [1, 2, 3, 4]
        costs = [1, 2, 3, 4]
        weight_limit = 4
        result = brute_force(weights, costs, weight_limit)
        self.assertEqual(result[COST], 4)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit,
                                             result))

    def test_5(self):
        """Проверка решения задачи о рюкзаке для пяти предметов."""
        weights = [10, 5, 12, 4, 2]
        costs = [5, 5, 3, 8, 6]
        weight_limit = 20
        result = brute_force(weights, costs, weight_limit)
        self.assertEqual(result[COST], 19)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit,
                                             result))

    def test_6(self):
        """Проверка решения задачи о рюкзаке для шести предметов."""
        weights = [10, 5, 12, 4, 2, 2]
        costs = [5, 5, 3, 8, 6, 8]
        weight_limit = 20
        result = brute_force(weights, costs, weight_limit)
        self.assertEqual(result[COST], 27)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit,
                                             result))

    def test_7(self):
        """Проверка решения задачи о рюкзаке для семи предметов."""
        weights = [10, 6, 11, 4, 1, 4, 3]
        costs = [15, 10, 22, 7, 1, 9, 4]
        weight_limit = 20
        result = brute_force(weights, costs, weight_limit)
        self.assertEqual(result[COST], 39)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit,
                                             result))


if __name__ == '__main__':
    unittest.main()
