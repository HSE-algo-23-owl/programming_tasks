import random
import random as rnd
import copy
from knapsack_problem.constants import COST, ITEMS, POPULATION_LIMIT, EPOCH_CNT, \
    BRUTE_FORCE_BOUND
from knapsack_problem.brute_force import brute_force
from knapsack_problem.validate import validate_params
from knapsack_problem.tournament import tournament


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
        self.__parents = self.find_parents()
        self.__prev_pop_w_children = self.find_children()
        self.__leaders = []

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции. Для каждой особи
        возвращается строка из 0 и 1, а также значение финтес-функции.
        """
        return self.__population

    def find_leader(self):
        self.__leaders.append(max(self.__population, key=lambda x: x[1])[0])

    def check_finish(self):
        if len(self.__leaders) >= 5 and self.__leaders[-1] == self.__leaders[-2] == self.__leaders[-3] == self.__leaders[-4] == self.__leaders[-5]:
            return True
        return False

    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> dict[str, int | list[int]]:
        """Запускает генетический алгоритм для решения задачи о рюкзаке.
        Алгоритм выполняется заданное количество поколений.

        :return: Словарь с ключами: cost - максимальная стоимость предметов в
        рюкзаке, items - список с индексами предметов, обеспечивающих максимальную
        стоимость.
        """
        if len(self.__weights) <= BRUTE_FORCE_BOUND:
            return brute_force(self.__weights, self.__costs, self.__weight_limit)  # Решение перебором

        while not self.check_finish() and epoch_cnt != 0:
            self.find_parents()
            self.find_children()
            self.make_new_population()
            self.find_leader()
            epoch_cnt -= 1

        leader = self.__leaders[-1]
        cost = self.find_fitness_function(leader)
        items = []
        for i in range(len(leader)):
            if leader[i] == '1':
                items.append(i)
        return {"cost": cost, "items": items}

    def mutation(self, population, item) -> str:
        """Мутирует особь так, чтобы новая особь не существовала в популяции и её вес предметов не превышал лимит
        рюкзака"""
        attempt1 = 0
        while (not (self.weight_check(item)) or any(tuple[0] == item for tuple in population)) and attempt1 < 10:
            attempt1 += 1
            attempt2, attempt3 = 0, 0
            while not (self.weight_check(item)) and attempt2 < 10:
                index = rnd.randint(0, len(self.__weights) - 1)
                if item[index] == '1':
                    item = item[:index] + "0" + item[index + 1:]
                attempt2 += 1
            while any(tuple[0] == item for tuple in population) and attempt3 < 10:
                index = rnd.randint(0, len(self.__weights) - 1)
                if item[index] == '1':
                    item = item[:index] + "0" + item[index + 1:]
                else:
                    item = item[:index] + "1" + item[index + 1:]
                attempt3 += 1
        if not (self.weight_check(item)) or any(tuple[0] == item for tuple in population):
            return ''
        return item

    def make_new_population(self):
        prev = sorted(self.__prev_pop_w_children, key=lambda x: x[1], reverse=True)
        self.__population = prev[0:int(self.__population_cnt)]


    def find_children(self):
        children = []
        parents = copy.deepcopy(self.__parents)
        parents_w_children = copy.deepcopy(self.__population)
        while len(parents)>1:
            f = parents.pop(0)
            s = parents.pop(0)
            numbers = ['0', '1']
            f_child, s_child = '', ''
            for j in range(len(self.__weights)):
                r = rnd.choice(numbers)
                if r == '1':
                    f_child += f[0][j]
                    s_child += s[0][j]
                else:
                    f_child += s[0][j]
                    s_child += f[0][j]
            f_child = self.mutation(parents_w_children, f_child)
            if f_child != '':
                parents_w_children.append((f_child, self.find_fitness_function(f_child)))
                children.append((f_child, self.find_fitness_function(f_child)))
            s_child = self.mutation(parents_w_children, s_child)
            if s_child != '':
                parents_w_children.append((s_child, self.find_fitness_function(s_child)))
                children.append((s_child, self.find_fitness_function(s_child)))
        self.__prev_pop_w_children = parents_w_children

        return parents_w_children

    def find_fitness_function(self, item) -> int:
        """Находит фитнес-функцию особи.
        :return: f - фитнес-функция особи"""
        f = 0
        for i in range(len(item)):
            if item[i] == '1':
                f += self.__costs[i]
        return f

    def find_parents(self):
        competitors = copy.deepcopy(self.__population)
        winners = []
        l = self.__population_cnt
        while len(winners) < len(self.population) // 2:
            comp = []
            for i in range(2):
                random_n = random.randint(0, l - 1)
                comp.append(competitors[random_n])
                competitors.pop(random_n)
                l -= 1
            winner = tournament(list(comp),
                                lambda x, y: x if self.find_fitness_function(x) > self.find_fitness_function(y) else y)
            winners.append(winner)

        self.__parents = winners
        return winners

    def weight_check(self, item):
        """Проверяет особь на то, вышли ли предметы за весовой предел рюкзака.
        :return: True - если предметы помещаются в рюкзак
        :return: False - если предметы не помещаются в рюкзак.
        """
        weight = 0
        for i in range(len(item)):
            if item[i] == '1':
                weight += self.__weights[i]
        if weight > self.__weight_limit:
            return False
        return True

    def __generate_population(self, __population_cnt):
        """Возвращает список особей начальной популяции. Для каждой особи
                возвращается строка из 0 и 1, а также значение фитнес-функции."""
        numbers = ['0', '1']
        population = []
        cnt = 0
        attempt = 0
        while cnt < self.__population_cnt and attempt < __population_cnt * 10:
            child = ''
            fitness_function = 0
            for j in range(len(self.__weights)):
                r = rnd.choice(numbers)
                child += r
                if r == '1':
                    fitness_function += self.__costs[j]
            if not any(tuple[0] == child for tuple in population) and self.weight_check(child):
                population.append((child, fitness_function))
                cnt += 1
            else:
                attempt += 1
        if len(population) < self.__population_cnt:
            self.__population_cnt = len(population)

        return population


if __name__ == '__main__':
    weights = [67, 30, 8, 50, 94, 24, 3, 78]
    costs = [77, 13, 38, 86, 92, 33, 46, 9]
    weight_limit = 50
    gk = GeneticSolver(weights, costs, weight_limit)
    print(gk.get_knapsack())
