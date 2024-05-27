import unittest

from main import get_knapsack, COST, ITEMS, ERR_LENGTHS_NOT_EQUAL, \
    ERR_NOT_INT_WEIGHT_LIMIT, ERR_NOT_POS_WEIGHT_LIMIT, ERR_LESS_WEIGHT_LIMIT, \
    ERR_NOT_LIST_TEMPL, ERR_EMPTY_LIST_TEMPL, ERR_NOT_INT_TEMPL, WEIGHTS, \
    COSTS, ERR_NOT_POS_TEMPL


class TestKnapsack(unittest.TestCase):
    @staticmethod
    def __check_set(weights: list[int], costs: list[int],
                    weight_limit: int, result: dict[str, int | list[int]]) -> (
            bool):
        """Проверяет набор предметов для рюкзака."""
        items_cnt = len(weights)
        cost = result[COST]
        items = result[ITEMS]
        if len(items) > items_cnt:
            return False
        if len(items) == 0:
            return False
        sum_cost = 0
        sum_weight = 0
        for idx in items:
            if idx >= items_cnt:
                return False
            sum_cost += costs[idx]
            sum_weight += weights[idx]
        if sum_weight > weight_limit:
            return False
        if sum_cost != cost:
            return False
        return True

    def test_not_list_weights(self):
        """Проверяет выброс исключения при передаче некорректного списка
        весов."""
        with self.assertRaises(TypeError) as error:
            get_knapsack(1, [1, 1], 1)
        self.assertEqual(ERR_NOT_LIST_TEMPL.format(WEIGHTS),
                         str(error.exception))

    def test_not_list_costs(self):
        """Проверяет выброс исключения при передаче некорректного списка
        стоимостей."""
        with self.assertRaises(TypeError) as error:
            get_knapsack([1], 'str', 1)
        self.assertEqual(ERR_NOT_LIST_TEMPL.format(COSTS),
                         str(error.exception))

    def test_empty_weights(self):
        """Проверяет выброс исключения при передаче пустого списка
        весов."""
        with self.assertRaises(ValueError) as error:
            get_knapsack([], [1, 1], 1)
        self.assertEqual(ERR_EMPTY_LIST_TEMPL.format(WEIGHTS),
                         str(error.exception))

    def test_empty_costs(self):
        """Проверяет выброс исключения при передаче пустого списка
        стоимостей."""
        with self.assertRaises(ValueError) as error:
            get_knapsack([1], [], 1)
        self.assertEqual(ERR_EMPTY_LIST_TEMPL.format(COSTS),
                         str(error.exception))

    def test_not_int_in_weights(self):
        """Проверяет выброс исключения при передаче нечислового значения
         в списке весов."""
        with self.assertRaises(TypeError) as error:
            get_knapsack([1, 'str'], [1, 1], 1)
        self.assertEqual(ERR_NOT_INT_TEMPL.format(WEIGHTS),
                         str(error.exception))

    def test_not_int_in_costs(self):
        """Проверяет выброс исключения при передаче нечислового значения
         в списке стоимостей."""
        with self.assertRaises(TypeError) as error:
            get_knapsack([1], [0.1], 1)
        self.assertEqual(ERR_NOT_INT_TEMPL.format(COSTS),
                         str(error.exception))

    def test_zero_in_weights(self):
        """Проверяет выброс исключения при передаче нулевого значения
         в списке весов."""
        with self.assertRaises(ValueError) as error:
            get_knapsack([1, 0], [1, 1], 1)
        self.assertEqual(ERR_NOT_POS_TEMPL.format(WEIGHTS),
                         str(error.exception))

    def test_zero_in_costs(self):
        """Проверяет выброс исключения при передаче нулевого значения
         в списке стоимостей."""
        with self.assertRaises(ValueError) as error:
            get_knapsack([1], [0], 1)
        self.assertEqual(ERR_NOT_POS_TEMPL.format(COSTS),
                         str(error.exception))

    def test_neg_in_weights(self):
        """Проверяет выброс исключения при передаче отрицательного значения
         в списке весов."""
        with self.assertRaises(ValueError) as error:
            get_knapsack([1, -1], [1, 1], 1)
        self.assertEqual(ERR_NOT_POS_TEMPL.format(WEIGHTS),
                         str(error.exception))

    def test_neg_in_costs(self):
        """Проверяет выброс исключения при передаче отрицательного значения
         в списке стоимостей."""
        with self.assertRaises(ValueError) as error:
            get_knapsack([1], [-10], 1)
        self.assertEqual(ERR_NOT_POS_TEMPL.format(COSTS),
                         str(error.exception))

    def test_diff_len(self):
        """Проверяет выброс исключения при передаче списков весов и
        стоимостей разной длины."""
        with self.assertRaises(ValueError) as error:
            get_knapsack([1], [1, 1], 1)
        self.assertEqual(ERR_LENGTHS_NOT_EQUAL, str(error.exception))

    def test_not_int_limit(self):
        """Проверяет выброс исключения при указании нечислового ограничения
        вместимости рюкзака."""
        with self.assertRaises(TypeError) as error:
            get_knapsack([1], [1], 1.1)
        self.assertEqual(ERR_NOT_INT_WEIGHT_LIMIT, str(error.exception))

    def test_zero_limit(self):
        """Проверяет выброс исключения при указании нулевого ограничения
        вместимости рюкзака."""
        with self.assertRaises(ValueError) as error:
            get_knapsack([1], [1], 0)
        self.assertEqual(ERR_NOT_POS_WEIGHT_LIMIT, str(error.exception))

    def test_neg_limit(self):
        """Проверяет выброс исключения при указании отрицательного ограничения
        вместимости рюкзака."""
        with self.assertRaises(ValueError) as error:
            get_knapsack([1], [1], -2)
        self.assertEqual(ERR_NOT_POS_WEIGHT_LIMIT, str(error.exception))

    def test_min_limit(self):
        """Проверяет выброс исключения при указании ограничения вместимости
        рюкзака менее чем минимальный вес предмета."""
        with self.assertRaises(ValueError) as error:
            get_knapsack([2], [1], 1)
        self.assertEqual(ERR_LESS_WEIGHT_LIMIT, str(error.exception))

    def test_2(self):
        """Проверка решения задачи о рюкзаке для двух предметов."""
        weights = [1, 1]
        costs = [1, 2]
        weight_limit = 1
        result = get_knapsack(weights, costs, weight_limit)
        self.assertEqual(result[COST], 2)
        self.assertTrue(TestKnapsack.__check_set(weights, costs, weight_limit,
                                                 result))

    def test_3(self):
        """Проверка решения задачи о рюкзаке для трех предметов."""
        weights = [1, 1, 2]
        costs = [1, 2, 2]
        weight_limit = 2
        result = get_knapsack(weights, costs, weight_limit)
        self.assertEqual(result[COST], 3)
        self.assertTrue(TestKnapsack.__check_set(weights, costs, weight_limit,
                                                 result))

    def test_4(self):
        """Проверка решения задачи о рюкзаке для четырех предметов."""
        weights = [1, 2, 3, 4]
        costs = [1, 2, 3, 4]
        weight_limit = 4
        result = get_knapsack(weights, costs, weight_limit)
        self.assertEqual(result[COST], 4)
        self.assertTrue(TestKnapsack.__check_set(weights, costs, weight_limit,
                                                 result))

    def test_5(self):
        """Проверка решения задачи о рюкзаке для пяти предметов."""
        weights = [10, 5, 12, 4, 2]
        costs = [5, 5, 3, 8, 6]
        weight_limit = 20
        result = get_knapsack(weights, costs, weight_limit)
        self.assertEqual(result[COST], 19)
        self.assertTrue(TestKnapsack.__check_set(weights, costs, weight_limit,
                                                 result))

    def test_6(self):
        """Проверка решения задачи о рюкзаке для шести предметов."""
        weights = [10, 5, 12, 4, 2, 2]
        costs = [5, 5, 3, 8, 6, 8]
        weight_limit = 20
        result = get_knapsack(weights, costs, weight_limit)
        self.assertEqual(result[COST], 27)
        self.assertTrue(TestKnapsack.__check_set(weights, costs, weight_limit,
                                                 result))

    def test_7(self):
        """Проверка решения задачи о рюкзаке для семи предметов."""
        weights = [10, 6, 11, 4, 1, 4, 3]
        costs = [15, 10, 22, 7, 1, 9, 4]
        weight_limit = 20
        result = get_knapsack(weights, costs, weight_limit)
        self.assertEqual(result[COST], 39)
        self.assertTrue(TestKnapsack.__check_set(weights, costs, weight_limit,
                                                 result))

    def test_max_items_exceeded(self):
        weights = [11, 4, 8, 6, 3, 5, 5, 7, 2, 10, 12, 9, 14, 1, 15, 13, 18, 17, 16, 19, 20]
        costs = [17, 6, 11, 10, 5, 8, 6, 13, 2, 15, 16, 9, 14, 1, 12, 13, 19, 18, 17, 20, 21]
        weight_limit = 50
        max_items = 20
        with self.assertRaises(ValueError) as context:
            get_knapsack(weights, costs, weight_limit, max_items)
        self.assertEqual(str(context.exception), f'Количество предметов превышает {max_items}')


if __name__ == '__main__':
    unittest.main()
