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

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции. Для каждой особи
        возвращается строка из 0 и 1, а также значение финтес-функции.
        """
        return self.__population

    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> dict[str, int | list[int]]:
        """Запускает генетический алгоритм для решения задачи о рюкзаке.
        Алгоритм выполняется заданное количество поколений.

        :return: Словарь с ключами: cost - максимальная стоимость предметов в
        рюкзаке, items - список с индексами предметов, обеспечивающих максимальную
        стоимость.
        """
        if len(self.__weights) <= BRUTE_FORCE_BOUND:
            return brute_force(self.__weights, self.__costs, self.__weight_limit)  # Решение перебором
        children = self.find_children()

    def mutation(self, population, item) -> str:
        """Мутирует особь так, чтобы новая особь не существовала в популяции и её вес предметов не превышал лимит
        рюкзака"""
        while not (self.weight_check(item)) or any(tuple[0] == item for tuple in population):
            while not (self.weight_check(item)):
                index = rnd.randint(0, len(weights) - 1)
                if item[index] == '1':
                    item = item[:index] + "0" + item[index + 1:]
            while any(tuple[0] == item for tuple in population):

                index = rnd.randint(0, len(weights)-1)
                if item[index] == '1':
                    item = item[:index] + "0" + item[index + 1:]
                else:
                    item = item[:index] + "1" + item[index + 1:]
        print(item)
        return item

    def find_children(self):
        children = []
        parents = copy.deepcopy(self.__parents)
        parents_w_children = copy.deepcopy(self.__population)
        while parents:
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
            parents_w_children.append((f_child, self.find_fitness_function(f_child)))
            children.append((f_child, self.find_fitness_function(f_child)))
            s_child = self.mutation(parents_w_children, s_child)
            parents_w_children.append((s_child, self.find_fitness_function(s_child)))
            children.append((s_child, self.find_fitness_function(s_child)))
        print("Дети")
        print(len(children), children)

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
        while len(winners) < len(self.population) // 2:  # отбираем половину популяции
            winner = tournament(list(competitors),
                                lambda x, y: x if self.find_fitness_function(x) > self.find_fitness_function(y) else y)
            winners.append(winner)
            competitors.remove(winner)
        print(f"Родители, {len(winners)} {winners}")
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
        while cnt < self.__population_cnt:
            child = ''
            fitness_function = 0
            for j in range(len(self.__weights)):
                r = rnd.choice(numbers)
                child += r
                if r == '1':
                    fitness_function += self.__costs[j]
            if child not in population or self.weight_check(child):
                population.append((child, fitness_function))
                cnt += 1
        return population


if __name__ == '__main__':
    weights = [67, 30, 8, 50, 94, 24, 3, 78]
    costs = [77, 13, 38, 86, 92, 33, 46, 9]
    weight_limit = 50
    gk = GeneticSolver(weights, costs, weight_limit)
    print(gk.get_knapsack())
