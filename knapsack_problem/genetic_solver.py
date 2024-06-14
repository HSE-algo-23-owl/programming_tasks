import random as rnd
from knapsack_problem.constants import COST, ITEMS, POPULATION_LIMIT, EPOCH_CNT, BRUTE_FORCE_BOUND
from knapsack_problem.brute_force import brute_force
from knapsack_problem.validate import validate_params


class GeneticSolver:
    """Класс для решения задачи о рюкзаке с использованием генетического
    алгоритма. Для входных данных небольшого размера используется полный перебор.
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
        return [(k, v) for k, v in self.__population.items()]

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
            new_items = self.__get_descendes(best_items)
            self.__update_population(new_items)

        return self.__get_best_result()

    def __get_best_result(self):
        best = max(self.__population.items(), key=lambda x: x[1])
        best_items = []
        for idx, bit in enumerate(best[0]):
            if bit == '1':
                best_items.append(idx)
        return {'cost': best[1], 'items': best_items}

    def __get_best_items(self) -> list[str]:
        population_items = list(self.__population.items())
        sorted_population = sorted(population_items, key=lambda item: item[1], reverse=True)
        num_best_items = len(self.__population) // 2
        best_half_population = sorted_population[:num_best_items]
        best_items = [k for k, v in best_half_population]
        return best_items

    def __get_descendes(self, items: list[str]) -> list[str]:
        new_items = []
        for first_idx in range(0, len(items) - len(items) % 2, 2):
            attempt_limit = 1000
            first = items[first_idx]
            second = items[first_idx + 1]
            first_child, second_child = self.__cross(first, second)
            while self.__get_fit(first_child) == 0 and attempt_limit > 0:
                first_child = self.__mutate(first_child)
                attempt_limit -= 1
            attempt_limit = 1000
            while self.__get_fit(second_child) == 0 and attempt_limit > 0:
                second_child = self.__mutate(second_child)
                attempt_limit -= 1
            if self.__get_fit(first_child) > 0:
                new_items.append(first_child)
            if self.__get_fit(second_child) > 0:
                new_items.append(second_child)
        return new_items

    def __cross(self, first: str, second: str) -> tuple[str, str]:
        point = rnd.randint(1, self.__item_cnt - 1)
        return first[:point] + second[point:], second[:point] + first[point:]

    def __mutate(self, item: str) -> str:
        idx = rnd.randint(0, self.__item_cnt - 1)
        mutated = list(item)
        mutated[idx] = '1' if mutated[idx] == '0' else '0'
        return ''.join(mutated)

    def __update_population(self, new_items: list[str]):
        new_population = {item: self.__get_fit(item) for item in new_items}
        sorted_items = self.__get_sorted_items()
        cur_idx = 0
        while len(new_population) < self.__population_cnt and cur_idx < len(sorted_items):
            item = sorted_items[cur_idx]
            cur_idx += 1
            new_population[item] = self.__get_fit(item)
        self.__population = new_population

    def __get_sorted_items(self) -> list[str]:
        population_items = list(self.__population.items())
        sorted_population = sorted(population_items, key=lambda item: item[1], reverse=True)
        best_items = [k for k, v in sorted_population]
        return best_items

    def __generate_population(self, population_cnt: int) -> dict[str, int]:
        population = {}
        while len(population) < population_cnt:
            item = self.__generate_item()
            if item not in population:
                population[item] = self.__get_fit(item)
        return population

    def __generate_item(self) -> str:
        return self.__mask.format(rnd.randint(0, 2**self.__item_cnt - 1))

    def __get_fit(self, item: str) -> int:
        total_weight = 0
        total_cost = 0
        for idx, bit in enumerate(item):
            if bit == '1':
                total_weight += self.__weights[idx]
                total_cost += self.__costs[idx]
        if total_weight <= self.__weight_limit:
            return total_cost
        else:
            return 0

if __name__ == '__main__':
    weights = [67, 30, 8, 50, 94, 24, 3, 78]
    costs = [77, 13, 38, 86, 92, 33, 46, 9]
    weight_limit = 50
    gk = GeneticSolver(weights, costs, weight_limit)
    print(gk.get_knapsack())
