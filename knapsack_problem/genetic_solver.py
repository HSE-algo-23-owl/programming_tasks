import random as rnd

from knapsack_problem.constants import COST, ITEMS, POPULATION_LIMIT, EPOCH_CNT, \
    BRUTE_FORCE_BOUND
from knapsack_problem.brute_force import brute_force
from knapsack_problem.validate import validate_params


class GeneticSolver:

    def __init__(self, weights: list[int], costs: list[int], weight_limit: int, max_stagnation: int = 50):
        validate_params(weights, costs, weight_limit)
        self.__item_cnt = len(weights)
        self.__mask = '{0:0' + str(len(weights)) + 'b}'
        self.__weights = weights
        self.__costs = costs
        self.__weight_limit = weight_limit
        self.__population_cnt = min(2 ** self.__item_cnt // 2, POPULATION_LIMIT)
        self.__population = self.__generate_population(self.__population_cnt)
        self.__max_stagnation = max_stagnation

    def __generate_population(self, population_size: int) -> list[str]:
        return [self.__mask.format(rnd.randint(0, 2 ** self.__item_cnt - 1)) for _ in range(population_size)]

    def __fitness(self, individual: str) -> int:
        total_weight = total_cost = 0
        for i, bit in enumerate(individual):
            if bit == '1':
                total_weight += self.__weights[i]
                total_cost += self.__costs[i]
        if total_weight > self.__weight_limit:
            return 0
        return total_cost

    def __select_parents(self, population: list[str], fitness_scores: list[int]) -> list[str]:
        total_fitness = sum(fitness_scores)
        if total_fitness == 0:
            return rnd.choices(population, k=2)
        selection_probs = [fitness / total_fitness for fitness in fitness_scores]
        return rnd.choices(population, weights=selection_probs, k=2)

    def __tournament_selection(self, population: list[str], fitness_scores: list[int], k: int = 3) -> str:
        selected = rnd.sample(list(zip(population, fitness_scores)), k)
        return max(selected, key=lambda x: x[1])[0]

    def __uniform_crossover(self, parent1: str, parent2: str) -> tuple[str, str]:
        offspring1, offspring2 = [], []
        for gene1, gene2 in zip(parent1, parent2):
            if rnd.random() > 0.5:
                offspring1.append(gene1)
                offspring2.append(gene2)
            else:
                offspring1.append(gene2)
                offspring2.append(gene1)
        return ''.join(offspring1), ''.join(offspring2)

    def __mutate(self, individual: str) -> str:
        individual = list(individual)
        point = rnd.randint(0, self.__item_cnt - 1)
        individual[point] = '1' if individual[point] == '0' else '0'
        return ''.join(individual)

    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> dict[str, int | list[int]]:
        best_individual = None
        best_fitness = -float('inf')
        stagnation_counter = 0

        for _ in range(epoch_cnt):
            fitness_scores = [self.__fitness(individual) for individual in self.__population]
            new_population = []

            for _ in range(self.__population_cnt // 2):
                parent1 = self.__tournament_selection(self.__population, fitness_scores)
                parent2 = self.__tournament_selection(self.__population, fitness_scores)
                offspring1, offspring2 = self.__uniform_crossover(parent1, parent2)
                new_population.extend([self.__mutate(offspring1), self.__mutate(offspring2)])

            self.__population = new_population
            current_best_individual = max(self.__population, key=self.__fitness)
            current_best_fitness = self.__fitness(current_best_individual)

            if current_best_fitness > best_fitness:
                best_individual = current_best_individual
                best_fitness = current_best_fitness
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            if stagnation_counter >= self.__max_stagnation:
                break

        best_items = [i for i, bit in enumerate(best_individual) if bit == '1']
        return {"cost": best_fitness, "items": best_items}




if __name__ == '__main__':
    weights = [67, 30, 8, 50, 94, 24, 3, 78]
    costs = [77, 13, 38, 86, 92, 33, 46, 9]
    weight_limit = 50
    gk = GeneticSolver(weights, costs, weight_limit)
    print(gk.get_knapsack())
