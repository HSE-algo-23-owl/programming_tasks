import random
import random as rnd

from knapsack_problem.constants import COST, ITEMS, POPULATION_LIMIT, EPOCH_CNT, \
    BRUTE_FORCE_BOUND
from knapsack_problem.brute_force import brute_force
from knapsack_problem.validate import validate_params


class GeneticSolver:
    """Класс для решения задачи о рюкзаке с использованием генетического
    алгоритма. Для входных данных небольшого размера используется полный
    перебор.

    Экземпляр класса хранит состояние популяции, метод поиска решения может
    быть запущен многократно для одного экземпляра.

    """

    def __init__(self, weights: list[int], costs: list[int], weight_limit: int):
        """Создает объект класса для решения задачи о рюкзаке.

        :param weights: Список весов предметов для рюкзака.
        :param costs: Список стоимостей предметов для рюкзака.
        :param weight_limit: Ограничение вместимости рюкзака.
        :raise TypeError: Если веса или стоимости не являются списком с числовыми
        значениями, если ограничение вместимости не является целым числом.
        :raise ValueError: Если в списках присутствует нулевое или отрицательное
        значение.
        """
        validate_params(weights, costs, weight_limit)
        self.__item_cnt = len(weights)
        self.__mask = '{0:0' + str(len(weights)) + 'b}'
        self.__weights = weights
        self.__costs = costs
        self.__weight_limit = weight_limit
        self.__population_cnt = min(2 ** self.__item_cnt / 2, POPULATION_LIMIT)
        self.__population = self.__generate_population(self.__population_cnt)

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции. Для каждой особи
        возвращается строка из 0 и 1, а также значение финтес-функции.
        """
        return [(self.__mask.format(item), fit) for item, fit in self.__population.items()]

    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> dict[str, int | list[int]]:
        """Запускает генетический алгоритм для решения задачи о рюкзаке.
        Алгоритм выполняется заданное количество поколений.

        :return: Словарь с ключами: cost - максимальная стоимость предметов в
        рюкзаке, items - список с индексами предметов, обеспечивающих максимальную
        стоимость.
        """
        if self.__item_cnt <= BRUTE_FORCE_BOUND:
            return brute_force(self.__weights, self.__costs, self.__weight_limit)

        for _ in range(epoch_cnt):
            best_items = self.__get_best_items()
            new_items = self.__get_new_items(best_items)
            self.__update_population(new_items)
        return self.__get_best_result()

    def __generate_population(self, population_cnt):
        attempt_limit = 1000
        population = {}
        item = self.__generate_valid_item()
        population[item] = self.__get_fit(item)
        while len(population) < population_cnt and attempt_limit:
            item = self.__generate_valid_item()
            population[item] = self.__get_fit(item)
            attempt_limit -= 1
        return population

    def __generate_valid_item(self):
        while True:
            item = []
            for _ in range(self.__item_cnt):
                item.append(random.randint(0, 1))
            item_int = int(''.join(map(str, item)), 2)
            if self.__calculate_weight(item) <= self.__weight_limit:
                return item_int

    def __calculate_weight(self, item: list[int]) -> int:
        total_weight = 0
        for i, isTake in enumerate(item):
            if isTake == 1:
                total_weight += self.__weights[i]
        return total_weight

    def __get_fit(self, item: int) -> int:
        item_str = self.__mask.format(item)
        total_weight = 0
        total_cost = 0
        for i, isTake in enumerate(item_str):
            if isTake == '1':
                total_weight += self.__weights[i]
                total_cost += self.__costs[i]

        if total_weight > self.__weight_limit:
            return 0
        return total_cost

    def __get_new_items(self, best_items: list[int]) -> list[int]:
        new_items = []
        for first_idx in range(1, len(best_items), 2):
            first = best_items[first_idx]
            second = best_items[first_idx - 1]
            first_child, second_child = self.__cross(first, second)

            attempt_limit = 1000
            while self.__get_fit(first_child) == 0 and attempt_limit:
                first_child = self.__mutate(first_child)
                attempt_limit -= 1
            if self.__get_fit(first_child) > 0 and self.__get_fit(first_child) != self.__get_fit(first):
                new_items.append(first_child)

            attempt_limit = 1000
            while self.__get_fit(second_child) == 0 and attempt_limit:
                second_child = self.__mutate(second_child)
                attempt_limit -= 1
            if self.__get_fit(second_child) > 0 and self.__get_fit(second_child) != self.__get_fit(second):
                new_items.append(second_child)

        return new_items

    def __mutate(self, item: int):
        while True:
            item_str = self.__mask.format(item)
            idx = random.randint(0, self.__item_cnt - 1)
            if bool(int(item_str[idx])):
                mutated_item = item - 2 ** (self.__item_cnt - idx - 1)
            else:
                mutated_item = item + 2 ** (self.__item_cnt - idx - 1)

            if self.__calculate_weight(self.__mask.format(mutated_item)) <= self.__weight_limit:
                return mutated_item


    def __update_population(self, new_items: list[int]) -> None:
        new_population = {}
        for item in new_items:
            new_population[item] = self.__get_fit(item)

        sorted_items = self.__get_sorted_items()
        item_idx = 0

        while (len(new_population) < self.__population_cnt and item_idx < len(sorted_items)):
            item = sorted_items[item_idx]
            new_population[item] = self.__get_fit(item)
            item_idx += 1

        self.__population = new_population

    def __get_sorted_items(self) -> list[int]:
        def fit_key(item):
            return item[1]

        sorted_population = sorted(self.__population.items(), key=fit_key, reverse=True)

        return [item[0] for item in sorted_population]

    def __cross(self, first: int, second: int) -> (int, int):
        while True:
            first_str = self.__mask.format(first)
            second_str = self.__mask.format(second)
            random_bound = random.randint(1, self.__item_cnt - 1)
            first_child = first_str[:random_bound] + second_str[random_bound:]
            second_child = second_str[:random_bound] + first_str[random_bound:]

            first_child_int = int(first_child, 2)
            second_child_int = int(second_child, 2)

            if (self.__calculate_weight(self.__mask.format(first_child_int)) <= self.__weight_limit and
                    self.__calculate_weight(self.__mask.format(second_child_int)) <= self.__weight_limit):
                return first_child_int, second_child_int

    def __get_best_result(self) -> dict[str, int | list[int]]:
        best_item = max(self.__population.items(), key=lambda x: x[1])
        best_item_str = self.__mask.format(best_item[0])
        items = [i for i, bit in enumerate(best_item_str) if bit == '1']
        return {
            'cost': best_item[1],
            'items': items
        }

    def __get_best_items(self) -> list[int]:
        sorted_population = self.__get_sorted_items()
        return sorted_population[:len(sorted_population) // 2]

if __name__ == '__main__':
    weights = [67, 30, 8, 50, 94, 24, 3, 78]
    costs = [77, 13, 38, 86, 92, 33, 46, 9]
    weight_limit = 50
    gk = GeneticSolver(weights, costs, weight_limit)
    print(gk.get_knapsack())
