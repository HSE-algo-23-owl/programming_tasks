import unittest
import random as rnd

from knapsack_problem.brute_force import brute_force
from knapsack_problem.genetic_solver import GeneticSolver
from knapsack_problem.constants import COST, BRUTE_FORCE_BOUND
from test import check_knapsack_items


class TestGeneticSolver(unittest.TestCase):
    """Набор тестов для проверки решения задачи о рюкзаке с использованием
    генетического алгоритма."""

    def test_simple(self):
        """Проверяет решение задачи на простом примере из 7 предметов."""
        weights = [10, 6, 11, 4, 1, 4, 3]
        costs = [15, 10, 22, 7, 1, 9, 4]
        weight_limit = 20
        gk = GeneticSolver(weights, costs, weight_limit)
        result = gk.get_knapsack()
        self.assertEqual(result[COST], 39)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit,
                                             result))

    def test_random_simple(self):
        """Проверяет решение задачи на 20 случайных наборах небольшого размера.
        Полученный результат проверяется с помощью полного перебора.
        Тест ожидает, что на небольших размерах входных данных генетический
        алгоритм найдет правильный ответ не менее чем в 19 из 20.
        """
        right_answer_cnt = 0
        for _ in range(20):
            items_cnt = rnd.randint(BRUTE_FORCE_BOUND, BRUTE_FORCE_BOUND + 10)
            weights = [rnd.randint(1, 100) for _ in range(items_cnt)]
            costs = [rnd.randint(1, 100) for _ in range(items_cnt)]
            weight_limit = rnd.randint(min(weights), sum(weights))
            gk = GeneticSolver(weights, costs, weight_limit)
            result = gk.get_knapsack()
            self.assertTrue(check_knapsack_items(weights, costs, weight_limit,
                                                 result))
            if result[COST] == brute_force(weights, costs, weight_limit)[COST]:
                right_answer_cnt += 1
                print("Решение совпало  ", right_answer_cnt)
            else:
                print("Не совпало")
        self.assertTrue(right_answer_cnt >= 19)

    def test_random_large(self):
        """Проверяет решение задачи на 20 случайных наборах большого размера
        (до 50 предметов).
        Полученный результат сравнивается со случайным набором предметов.
        Тест ожидает, что генетический алгоритм возвращает решение лучшее
         чем случайно выбранное не менее чем в 9 из 10.
         """
        better_than_random_answer_cnt = 0
        for _ in range(20):
            items_cnt = rnd.randint(BRUTE_FORCE_BOUND + 10, 50)
            weights = [rnd.randint(1, 100) for _ in range(items_cnt)]
            costs = [rnd.randint(1, 100) for _ in range(items_cnt)]
            weight_limit = rnd.randint(int(sum(weights) / 2), sum(weights))
            gk = GeneticSolver(weights, costs, weight_limit)
            result = gk.get_knapsack()
            self.assertTrue(check_knapsack_items(weights, costs, weight_limit,
                                                 result))
            random_set_cost = (
                TestGeneticSolver.__get_random_set_cost(weights, costs,
                                                        weight_limit))
            if result[COST] > random_set_cost:
                better_than_random_answer_cnt += 1
        self.assertTrue(better_than_random_answer_cnt >= 19)

    def test_random_progress(self):
        """Проверяет прогресс улучшения результата при работе генетического
        алгоритма. Чем дольше работает алгоритм, тем лучший результат будет
        получен.
        Тест получает первый результат после 2 поколений алгоритма, затем 10
        раз запускает выполнение по 20 поколений.
        Тест ожидает, что при каждом следующем запуске полученный результат не
        ухудшается, а последний результат строго лучше первого.
        """
        items_cnt = 50
        weights = [rnd.randint(20, 80) for _ in range(items_cnt)]
        costs = [rnd.randint(20, 80) for _ in range(items_cnt)]
        weight_limit = int(sum(weights) * 0.66)
        gk = GeneticSolver(weights, costs, weight_limit)
        first_result = gk.get_knapsack(2)
        last_result = None
        for i in range(10):
            last_result = gk.get_knapsack(20)
            self.assertTrue(last_result[COST] >= first_result[COST])
        self.assertTrue(last_result[COST] > first_result[COST])

    @staticmethod
    def __get_random_set_cost(weights, costs, weight_limit):
        """Генерирует случайный набор предметов, удовлетворяющий ограничению
        вместимости рюкзака, и возвращает его стоимость."""
        attempt = 0
        attempt_limit = 100
        mask = '{0:0' + str(len(weights)) + 'b}'
        items_cnt = len(weights)
        item_set = rnd.randint(1, 2 ** items_cnt)
        set_str = mask.format(item_set)
        weight = sum([weights[i] if bool(int(set_str[i])) else 0
                      for i in range(0, items_cnt)])
        while weight > weight_limit and attempt < attempt_limit:
            item_set = rnd.randint(1, 2 ** items_cnt)
            set_str = mask.format(item_set)
            weight = sum([weights[i] if bool(int(set_str[i])) else 0
                          for i in range(0, items_cnt)])
            attempt += 1
        if weight > weight_limit:
            return 0
        return sum([costs[i] if bool(int(set_str[i])) else 0
                    for i in range(0, items_cnt)])


if __name__ == '__main__':
    unittest.main()
