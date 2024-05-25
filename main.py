from __future__ import annotations

COST = 'cost'
ITEMS = 'items'
WEIGHTS = 'Веса'
COSTS = 'Стоимости'
ERR_LENGTHS_NOT_EQUAL = 'Списки весов и стоимости разной длины'
ERR_NOT_INT_WEIGHT_LIMIT = ('Ограничение вместимости рюкзака не является целым '
                            'числом')
ERR_NOT_POS_WEIGHT_LIMIT = 'Ограничение вместимости рюкзака меньше единицы'
ERR_LESS_WEIGHT_LIMIT = ('Ограничение вместимости рюкзака меньше чем '
                         'минимальный вес предмета')
ERR_NOT_LIST_TEMPL = '{0} не являются списком'
ERR_EMPTY_LIST_TEMPL = '{0} являются пустым списком'
ERR_NOT_INT_TEMPL = '{0} содержат не числовое значение'
ERR_NOT_POS_TEMPL = '{0} содержат нулевое или отрицательное значение'
MAX_ITEMS = 20
ERR_TOO_MANY_ITEMS = "Количество предметов не должно превышать 21"


def check_values(weights: list[int], costs: list[int], weight_limit: int):
    if not (type(weights) is list):
        raise TypeError(ERR_NOT_LIST_TEMPL.format(WEIGHTS))
    elif not (type(costs) is list):
        raise TypeError(ERR_NOT_LIST_TEMPL.format(COSTS))
    elif not weights:
        raise ValueError(ERR_EMPTY_LIST_TEMPL.format(WEIGHTS))
    elif not costs:
        raise ValueError(ERR_EMPTY_LIST_TEMPL.format(COSTS))
    elif not (all(type(item) is int for item in weights)):
        raise TypeError(ERR_NOT_INT_TEMPL.format(WEIGHTS))
    elif not (all(type(item) is int for item in costs)):
        raise TypeError(ERR_NOT_INT_TEMPL.format(COSTS))
    elif not (all(item > 0 for item in weights)):
        raise ValueError(ERR_NOT_POS_TEMPL.format(WEIGHTS))
    elif not (all(item > 0 for item in costs)):
        raise ValueError(ERR_NOT_POS_TEMPL.format(COSTS))
    elif len(weights) != len(costs):
        raise ValueError(ERR_LENGTHS_NOT_EQUAL)
    elif not (isinstance(weight_limit, int)):
        raise TypeError(ERR_NOT_INT_WEIGHT_LIMIT)
    elif weight_limit <= 0:
        raise ValueError(ERR_NOT_POS_WEIGHT_LIMIT)
    elif not (all(item <= weight_limit for item in weights)):
        raise ValueError(ERR_LESS_WEIGHT_LIMIT)
    elif len(weights) > MAX_ITEMS:
        raise ValueError(ERR_TOO_MANY_ITEMS)


def create_combination_bin(number_combination, combination_len):
    combination_partial_bin = bin(number_combination)[2:]
    combination_bin = list(map(int, ("0" * (combination_len - len(combination_partial_bin)) + combination_partial_bin)))
    combination = [i for i in range(0, combination_len) if combination_bin[i] == 1]
    return combination


def is_combination_valid(combination, weights, weight_limit):
    current_weight = 0
    for i in combination:
        current_weight += weights[i]
    if current_weight <= weight_limit:
        return True
    else:
        return False


def found_cost(combination, costs):
    current_cost = 0
    for i in combination:
        current_cost += costs[i]
    return current_cost


def get_knapsack(weights: list[int], costs: list[int], weight_limit: int) -> \
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
    check_values(weights, costs, weight_limit)
    max_cost = 0
    max_combination = []
    for number_to_combination in range(1, 2 ** (len(weights))):
        current_combination = create_combination_bin(number_to_combination, len(weights))
        if is_combination_valid(current_combination, weights, weight_limit):
            cost = found_cost(current_combination, costs)
            if cost > max_cost:
                max_cost = cost
                max_combination = current_combination
    return {COST: max_cost, ITEMS: max_combination}


if __name__ == '__main__':
    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    costs = [1, 1, 1, 1, 20, 1, 1, 1, 1, 20, 1, 1, 1, 1, 10, 1, 1, 1, 1, 21]
    weight_limit = 40
    print('Пример решения задачи о рюкзаке\n')
    print(f'Веса предметов для комплектования рюкзака: {weights}')
    print(f'Стоимости предметов для комплектования рюкзака: {costs}')
    print(f'Ограничение вместимости рюкзака: {weight_limit}')
    result = get_knapsack(weights, costs, weight_limit)
    print(f'Максимальная стоимость: {result[COST]}, '
          f'индексы предметов: {result[ITEMS]}')
