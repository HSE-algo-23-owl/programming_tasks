import random as rnd

from knapsack_problem.constants import COST, ITEMS, POPULATION_LIMIT, EPOCH_CNT, \
    BRUTE_FORCE_BOUND, ATTEMPTS, LEADER_STAGNATION_EPOCHS, MAX_GENES_TO_MUTATE
from knapsack_problem.brute_force import brute_force
from knapsack_problem.tournament import tournament
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
        return list(self.__population.items())

    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> dict[str, int | list[int]]:
        """Запускает генетический алгоритм для решения задачи о рюкзаке.
        Алгоритм выполняется заданное количество поколений.

        :return: Словарь с ключами: cost - максимальная стоимость предметов в
        рюкзаке, items - список с индексами предметов, обеспечивающих максимальную
        стоимость.
        """
        if self.__item_cnt <= BRUTE_FORCE_BOUND:
            return brute_force(self.__weights, self.__costs, self.__weight_limit)

        leader = self.__get_leader()
        leader_stagnation_epoch = 0

        while epoch_cnt and len(self.population) > 2 and leader_stagnation_epoch < LEADER_STAGNATION_EPOCHS:
            tournament_winners = self.__chromosome_selection()  # отбор особей для скрещивания турнирным методом
            descendants = self.__get_descendants(tournament_winners)  # скрещивание, формирование потомков
            self.__update_population(tournament_winners, descendants)  # обновление популяции, создание очередного поколения
            new_leader = self.__get_leader()

            if new_leader == leader:
                leader_stagnation_epoch += 1
            else:
                leader_stagnation_epoch = 0
                leader = new_leader

            epoch_cnt -= 1

        return leader

    def __get_leader(self) -> dict[str, int | list[int]]:
        """Получает лидера текущей популяции.

        :return: Словарь с ключами: cost - максимальная стоимость предметов в
        рюкзаке, items - список с индексами предметов, обеспечивающих максимальную
        стоимость.
        """
        # нахождение особи с максимальной фитнес-функцией
        leader_items, leader_cost = max(self.__population.items(), key=lambda x: x[1])
        return {COST: leader_cost, ITEMS: [i for i in range(len(leader_items)) if leader_items[i] == '1']}

    def __generate_population(self, population_cnt: int) -> dict[str, int]:
        """Создает первоначальную популяцию случайным образом.

        :param population_cnt: Количество особей в популяции.
        :return: Словарь с ключами: str - хромосома, int - фитнес-фукнция.
        """
        population = dict()
        attempts = ATTEMPTS

        while len(population) < population_cnt and attempts:
            attempts -= 1

            chromosome = self.__generate_chromosome()  # генерация особи
            fitness_func = self.__get_fitness_func(chromosome)  # получение фитнес-функции новой особи

            if chromosome in population or not fitness_func:
                continue

            population.setdefault(chromosome, fitness_func)

        return population

    def __generate_chromosome(self) -> str:
        """Генерирует хромосому псевдослучайным образом на основе алгоритма Вихря Мерсенна.

        :return: Хромосома в строковом виде.
        """
        return self.__mask.format(rnd.randint(1, 2**self.__item_cnt - 1))

    def __get_fitness_func(self, chromosome: str) -> int:
        """Высчитывает фитнес-функцию особи.

        :param chromosome: Код особи в строком виде.
        :return: Целое положительное число большее нуля, если вес предметов не превышает лимит, иначе 0.
        """
        # нахождение суммы весов всех предметов в рюкзаке и проверка на превышение объема рюкзака
        if sum(self.__weights[i] for i in range(len(chromosome)) if int(chromosome[i])) <= self.__weight_limit:
            return sum(self.__costs[i] for i in range(len(chromosome)) if int(chromosome[i]))  # суммарная стоимость предметов
        return 0

    def __chromosome_selection(self) -> list[str]:
        """Отбирает особей для скрещивания турнирным методом.

        :return: Список особей-победителей турнира.
        """
        competitors = set(self.__population)
        winners = set()
        while len(winners) < len(self.population) // 2:  # отбираем половину популяции
            winner = tournament(list(competitors), lambda x, y: x if self.__get_fitness_func(x) > self.__get_fitness_func(y) else y)
            winners.add(winner)
            competitors.discard(winner)
        return list(winners)

    def __get_descendants(self, tournament_winners: list[str]) -> list[str]:
        """Получает потомков путем скрещивания особей-родителей.

        :return: Список жизнеспособных потомков.
        """
        rnd.shuffle(tournament_winners)  # перемешивание особей
        tournament_winners = tournament_winners[:len(tournament_winners) // 2 * 2]  # срез для четного кол-ва особей
        attempts = ATTEMPTS
        descendants = set()

        for i in range(1, len(tournament_winners), 2):
            first_descendant, second_descendant = self.__uniform_crossing(tournament_winners[i-1], tournament_winners[i])

            while (first_descendant in descendants or not self.__get_fitness_func(first_descendant)) and attempts:
                first_descendant = self.__mutation(first_descendant)
                attempts -= 1

            attempts = ATTEMPTS

            while (second_descendant in descendants or not self.__get_fitness_func(second_descendant)) and attempts:
                second_descendant = self.__mutation(second_descendant)
                attempts -= 1

            if self.__get_fitness_func(first_descendant):  # добавление жизнеспособной особи-потомка во множество
                descendants.add(first_descendant)

            if self.__get_fitness_func(second_descendant):
                descendants.add(second_descendant)

        return list(descendants)

    @staticmethod
    def __mutation(chromosome: str) -> str:
        """Мутирует гены хромосомы.

        :param chromosome: Хромосома потомка.
        :return: Хромосома после проведения мутации.
        """
        chromosome = list(chromosome)
        modify_gene_cnt = rnd.randint(1, MAX_GENES_TO_MUTATE)  # рандомный выбор количества генов для мутации

        for pos in rnd.sample(range(len(chromosome)), modify_gene_cnt):
            chromosome[pos] = '1' if chromosome[pos] == '0' else '0'  # инверсия генов

        return ''.join(chromosome)

    def __uniform_crossing(self, first_parent: str, second_parent: str) -> tuple[str, str]:
        """Осуществляет равномерное скрещивание двух особей.

        :param first_parent: Хромосома первого родителя.
        :param first_parent: Хромосома второго родителя.
        :return: Кортеж из двух потомков.
        """
        pattern = self.__generate_chromosome()  # последовательность-шаблон для обмена генами на текущей позиции
        first_descendant, second_descendant = list(first_parent), list(second_parent)

        for i, gene in enumerate(pattern):
            if int(gene):
                first_descendant[i], second_descendant[i] = second_descendant[i], first_descendant[i]

        return ''.join(first_descendant), ''.join(second_descendant)

    def __update_population(self, tournament_winners: list[str], descendants: list[str]) -> None:
        """Обновляет популяцию, создает очередное поколение, состоящее из родителей и потомков.

        :param tournament_winners: Особи-родители, участвовавшиеся в скрещивании, победители турнира.
        :param descendants: Особи-потомки, получившиеся в результате скрещивания особей-родителей.
        """
        # новая популяция будет состоять из родителей и их потомков
        new_population, descendants = set(tournament_winners), set(descendants)

        # объединение родителей и потомков в одну популяцию в случае недобора нужного объема популяции
        if len(new_population) + len(descendants) <= POPULATION_LIMIT:
            new_population |= set(descendants)
        else:
            while len(new_population) < POPULATION_LIMIT:  # добавление потомков, пока есть свободное место
                new_population.add(descendants.pop())

        self.__population = {chromosome: self.__get_fitness_func(chromosome) for chromosome in new_population}


if __name__ == '__main__':
    weights = [67, 30, 8, 50, 94, 24, 3, 78]
    costs = [77, 13, 38, 86, 92, 33, 46, 9]
    weight_limit = 50
    gk = GeneticSolver(weights, costs, weight_limit)
    print(gk.get_knapsack())
