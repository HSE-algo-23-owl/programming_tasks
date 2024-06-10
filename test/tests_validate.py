import unittest

from knapsack_problem.brute_force import brute_force
from knapsack_problem.validate import validate_params
from knapsack_problem.constants import ERR_LENGTHS_NOT_EQUAL, \
    ERR_NOT_INT_WEIGHT_LIMIT, ERR_NOT_POS_WEIGHT_LIMIT, ERR_LESS_WEIGHT_LIMIT, \
    ERR_NOT_LIST_TEMPL, ERR_EMPTY_LIST_TEMPL, ERR_NOT_INT_TEMPL, \
    ERR_NOT_POS_TEMPL, COST, ITEMS, WEIGHTS, COSTS


class TestValidate(unittest.TestCase):
    """Набор тестов для проверки входных данных для задачи о рюкзаке."""

    def test_not_list_weights(self):
        """Проверяет выброс исключения при передаче некорректного списка
        весов."""
        with self.assertRaises(TypeError) as error:
            validate_params(1, [1, 1], 1)
        self.assertEqual(ERR_NOT_LIST_TEMPL.format(WEIGHTS),
                         str(error.exception))

    def test_not_list_costs(self):
        """Проверяет выброс исключения при передаче некорректного списка
        стоимостей."""
        with self.assertRaises(TypeError) as error:
            validate_params([1], 'str', 1)
        self.assertEqual(ERR_NOT_LIST_TEMPL.format(COSTS),
                         str(error.exception))

    def test_empty_weights(self):
        """Проверяет выброс исключения при передаче пустого списка
        весов."""
        with self.assertRaises(ValueError) as error:
            validate_params([], [1, 1], 1)
        self.assertEqual(ERR_EMPTY_LIST_TEMPL.format(WEIGHTS),
                         str(error.exception))

    def test_empty_costs(self):
        """Проверяет выброс исключения при передаче пустого списка
        стоимостей."""
        with self.assertRaises(ValueError) as error:
            validate_params([1], [], 1)
        self.assertEqual(ERR_EMPTY_LIST_TEMPL.format(COSTS),
                         str(error.exception))

    def test_not_int_in_weights(self):
        """Проверяет выброс исключения при передаче нечислового значения
         в списке весов."""
        with self.assertRaises(TypeError) as error:
            validate_params([1, 'str'], [1, 1], 1)
        self.assertEqual(ERR_NOT_INT_TEMPL.format(WEIGHTS),
                         str(error.exception))

    def test_not_int_in_costs(self):
        """Проверяет выброс исключения при передаче нечислового значения
         в списке стоимостей."""
        with self.assertRaises(TypeError) as error:
            validate_params([1], [0.1], 1)
        self.assertEqual(ERR_NOT_INT_TEMPL.format(COSTS),
                         str(error.exception))

    def test_zero_in_weights(self):
        """Проверяет выброс исключения при передаче нулевого значения
         в списке весов."""
        with self.assertRaises(ValueError) as error:
            validate_params([1, 0], [1, 1], 1)
        self.assertEqual(ERR_NOT_POS_TEMPL.format(WEIGHTS),
                         str(error.exception))

    def test_zero_in_costs(self):
        """Проверяет выброс исключения при передаче нулевого значения
         в списке стоимостей."""
        with self.assertRaises(ValueError) as error:
            validate_params([1], [0], 1)
        self.assertEqual(ERR_NOT_POS_TEMPL.format(COSTS),
                         str(error.exception))

    def test_neg_in_weights(self):
        """Проверяет выброс исключения при передаче отрицательного значения
         в списке весов."""
        with self.assertRaises(ValueError) as error:
            validate_params([1, -1], [1, 1], 1)
        self.assertEqual(ERR_NOT_POS_TEMPL.format(WEIGHTS),
                         str(error.exception))

    def test_neg_in_costs(self):
        """Проверяет выброс исключения при передаче отрицательного значения
         в списке стоимостей."""
        with self.assertRaises(ValueError) as error:
            validate_params([1], [-10], 1)
        self.assertEqual(ERR_NOT_POS_TEMPL.format(COSTS),
                         str(error.exception))

    def test_diff_len(self):
        """Проверяет выброс исключения при передаче списков весов и
        стоимостей разной длины."""
        with self.assertRaises(ValueError) as error:
            validate_params([1], [1, 1], 1)
        self.assertEqual(ERR_LENGTHS_NOT_EQUAL, str(error.exception))

    def test_not_int_limit(self):
        """Проверяет выброс исключения при указании нечислового ограничения
        вместимости рюкзака."""
        with self.assertRaises(TypeError) as error:
            validate_params([1], [1], 1.1)
        self.assertEqual(ERR_NOT_INT_WEIGHT_LIMIT, str(error.exception))

    def test_zero_limit(self):
        """Проверяет выброс исключения при указании нулевого ограничения
        вместимости рюкзака."""
        with self.assertRaises(ValueError) as error:
            validate_params([1], [1], 0)
        self.assertEqual(ERR_NOT_POS_WEIGHT_LIMIT, str(error.exception))

    def test_neg_limit(self):
        """Проверяет выброс исключения при указании отрицательного ограничения
        вместимости рюкзака."""
        with self.assertRaises(ValueError) as error:
            validate_params([1], [1], -2)
        self.assertEqual(ERR_NOT_POS_WEIGHT_LIMIT, str(error.exception))

    def test_min_limit(self):
        """Проверяет выброс исключения при указании ограничения вместимости
        рюкзака менее чем минимальный вес предмета."""
        with self.assertRaises(ValueError) as error:
            validate_params([2], [1], 1)
        self.assertEqual(ERR_LESS_WEIGHT_LIMIT, str(error.exception))


if __name__ == '__main__':
    unittest.main()
