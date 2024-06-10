from knapsack_problem.constants import COST, ITEMS
from knapsack_problem.genetic_solver import GeneticSolver

if __name__ == '__main__':
    weights = [56, 27, 56, 47, 29, 31, 31, 66, 49, 26, 65, 45, 51, 31, 73, 27,
               23, 26, 78, 25, 48, 78, 67, 79, 77, 69, 49, 78, 46, 79, 22, 33,
               55, 67, 47, 70, 28, 20, 73, 57, 26, 55, 50, 76, 43, 74, 39, 43,
               39, 50]
    costs = [53, 49, 74, 71, 40, 36, 28, 65, 32, 64, 39, 50, 58, 52, 67, 71, 69,
             47, 75, 25, 27, 72, 70, 39, 50, 58, 59, 77, 75, 35, 39, 74, 59, 20,
             74, 58, 33, 55, 75, 51, 46, 37, 70, 20, 35, 20, 79, 22, 46, 66]
    weight_limit = 1600
    print('Пример решения задачи о рюкзаке\n')
    print(f'Количество предметов для комплектования рюкзака: {len(weights)}')
    print(f'Суммарный вес предметов для комплектования рюкзака: {sum(weights)}')
    print(f'Ограничение вместимости рюкзака: {weight_limit}')
    gk = GeneticSolver(weights, costs, weight_limit)

    result = gk.get_knapsack(3)
    print(f'\nПроведем генерацию 3 поколений'
          f'\nМаксимальная стоимость: {result[COST]}, '
          f'индексы предметов: {result[ITEMS]}')

    result = gk.get_knapsack(10)
    print(f'\nПроведем генерацию еще 10 поколений'
          f'\nМаксимальная стоимость: {result[COST]}, '
          f'индексы предметов: {result[ITEMS]}')

    result = gk.get_knapsack(20)
    print(f'\nПроведем генерацию еще 20 поколений'
          f'\nМаксимальная стоимость: {result[COST]}, '
          f'индексы предметов: {result[ITEMS]}')

    result = gk.get_knapsack(100)
    print(f'\nПроведем генерацию еще 100 поколений'
          f'\nМаксимальная стоимость: {result[COST]}, '
          f'индексы предметов: {result[ITEMS]}')

    print(f'\nКоличество особей в популяции: {len(gk.population)}')
    for item in gk.population:
        print(item)
