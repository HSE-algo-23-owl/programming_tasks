"""Пакет для решения задачи о рюкзаке.

GeneticSolver - Класс для решения задачи о рюкзаке с использованием генетического
    алгоритма. Для входных данных небольшого размера используется полный
    перебор.

brute_force - метод для решения задачи о рюкзаке с использованием полного
перебора.

validate_params - метод для проверки входных данных задачи о рюкзаке.
"""


from knapsack_problem.genetic_solver import GeneticSolver
from knapsack_problem.brute_force import brute_force
from knapsack_problem.validate import validate_params


__all__ = ['GeneticSolver', 'brute_force', 'validate_params']
__version__ = '1.0.0'
__author__ = 'Alexander Mikhailov'
__license__ = 'MIT'
