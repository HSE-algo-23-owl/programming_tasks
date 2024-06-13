import random as rnd
import numpy as np

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
        weight_prob = []
        ost = 1
        for i in range(self.__item_cnt - 1):
            weight_prob.append(ost / 2)
            ost -= ost / 2
        weight_prob.append(ost)
        self.__prob = weight_prob

    @property
    def population(self, prev_population, children) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции. Для каждой особи
        возвращается строка из 0 и 1, а также значение фитнес-функции.
        """
        prev_population = sorted(prev_population, key=lambda x: x[1], reverse=True)
        population = prev_population[0:len(prev_population) // 2]
        prev_population = prev_population[len(prev_population) // 2::]
        for i in children:
            prev_population.append((i, self.find_fitness_function(children[i])))
        prev_population = sorted(prev_population, key=lambda x: x[1], reverse=True)
        length = len(population)
        for i in range(length, self.__population_cnt):
            population.append(prev_population.pop(0))
        return population

    def find_fitness_function(self, item):
        f = 0
        for i in range(len(item)):
            if item[i] == '1':
                f += self.__costs[i]
        return f

    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> dict[str, int | list[int]]:
        """Запускает генетический алгоритм для решения задачи о рюкзаке.
        Алгоритм выполняется заданное количество поколений.

        :return: Словарь с ключами: cost - максимальная стоимость предметов в
        рюкзаке, items - список с индексами предметов, обеспечивающих максимальную
        стоимость.
        """
        if BRUTE_FORCE_BOUND <= 5:
            return self.get_knapsack_full(self.__weights, self.__costs, self.__weight_limit)
        else:
            leaders = []
            first_population = self.__generate_population(self.__population_cnt)
            while True:
                leaders.append(max(first_population, key=lambda x: x[1])[0])
                parents = []
                for i in range(2):
                    while len(first_population) > 1:
                        f = first_population.pop(0)
                        s = first_population.pop()
                        if f[1] > s[1]:
                            parents.append(f)
                        else:
                            parents.append(s)
                    if len(first_population) == 1:
                        f = first_population.pop()
                        s = parents.pop()
                        if f[1] > s[1]:
                            parents.append(f)
                        else:
                            parents.append(s)
                    first_population, parents = parents, []
                parents = first_population
                if len(parents) % 2 == 1:
                    f = parents.pop()
                    s = parents.pop(-2)
                    if f[1] > s[1]:
                        parents.append(f)
                    else:
                        parents.append(s)
                children = []
                while parents:
                    f = parents.pop(0)
                    s = parents.pop(1)
                    fitness_function_f, fitness_function_s = 0, 0
                    numbers = ['0', '1']
                    f_child, s_child = '', ''
                    for j in range(len(weights)):
                        r = rnd.choice(numbers)
                        if r == '1':
                            f_child += f[j]
                            s_child += s[j]
                        else:
                            f_child += s[j]
                            s_child += f[j]
                    f_child, s_child = self.mutation(f_child, first_population), self.mutation(s_child, first_population)
                    children.append(f_child)
                    children.append(s_child)
                    first_population = self.__population(first_population, children)
                if len(leaders) >= 3 and leaders[-1] == leaders[-2] == leaders[-3]:
                    items = []
                    for i in range(len(leaders[-1])):
                        if leaders[-1][i] == '1':
                            items.append(len(weights) - i - 1)
                    return {"cost": self.find_fitness_function(leaders[-1]), "items": items}

    def weight_check(self, item):
        weight = 0
        for i in range(len(item)):
            if item[i] == '1':
                weight += self.__weights[i]
        if weight > self.__weight_limit:
            return False
        return True

    def mutation(self, population, item):
        while not (self.weight_check(item)) or item in population:
            while not (self.weight_check(item)):
                index = rnd.randint(0, len(weights))
                if item[index] == '1':
                    item = item[:index] + "0" + item[index + 1:]
            while item in population:
                index = rnd.randint(0, len(weights))
                if item[index] == '1':
                    item = item[:index] + "0" + item[index + 1:]
                else:
                    item = item[:index] + "1" + item[index + 1:]
        return item

    def get_knapsack_full(self, weights: list[int], costs: list[int], weight_limit: int) -> \
            dict[str, int | list[int]]:
        """Решает задачу о рюкзаке с использованием полного перебора.
        :param weights: Список весов предметов для рюкзака.
        :param costs: Список стоимостей предметов для рюкзака.
        :param weight_limit: Ограничение вместимости рюкзака.
        :raise TypeError: Если веса или стоимости не являются списком с числовыми
        значениями, если ограничение вместимости не является целым числом.
        :raise ValueError: Если в списках присутствует нулевое или отрицательное
        значение.
        :return: Словарь с ключами: cost - максимальная стоимость предметов в
        рюкзаке, items - список с индексами предметов, обеспечивающих максимальную
        стоимость.
        """
        all_variants = 2 ** len(weights) - 1
        max_cost = 0

        best_option_reverse = ''
        reverse_weight = weights[::-1]
        reverse_cost = costs[::-1]
        for i in range(1, all_variants + 1):
            variant = bin(i)[2::]
            reverse_variant = variant[::-1]
            l = len(variant)
            current_weight, current_cost = 0, 0
            for j in range(l):
                if reverse_variant[j] == '1':
                    current_weight += reverse_weight[j]
                    if current_weight > weight_limit:
                        current_cost = 0
                        break
                    current_cost += reverse_cost[j]
            if max_cost < current_cost:
                best_option_reverse = reverse_variant
                max_cost = current_cost
        items = []
        for i in range(len(best_option_reverse)):
            if best_option_reverse[i] == '1':
                items.append(len(weights) - i - 1)
        items.reverse()

        return {"cost": max_cost, "items": items}

    def __generate_population(self, __population_cnt):
        numbers = ['0', '1']
        population = []
        cnt = 0
        while cnt < self.__population_cnt:
            child = ''
            fitness_function, sum_weights = 0, 0
            for j in range(len(self.__weights)):
                r = rnd.choice(numbers)
                child += r
                if r == '1':
                    fitness_function += self.__costs[j]
                    sum_weights += self.__weights[j]
            if child not in population or sum_weights < self.__weight_limit:
                population.append((child, fitness_function))
                cnt += 1

        return population


if __name__ == '__main__':
    weights = [67, 30, 8, 50, 94, 24, 3, 78]
    costs = [77, 13, 38, 86, 92, 33, 46, 9]
    weight_limit = 50
    gk = GeneticSolver(weights, costs, weight_limit)
    print(gk.get_knapsack())
