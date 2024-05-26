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


def get_knapsack(weights: list[int], costs: list[int], weight_limit: int, max_items: int = 20) -> \
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
    if not isinstance(weights, list) or not isinstance(costs, list):
        raise TypeError(ERR_NOT_LIST_TEMPL.format('Веса' if not isinstance(weights, list) else 'Стоимости'))
    if not weights:
        raise ValueError(ERR_EMPTY_LIST_TEMPL.format('Веса'))
    if not costs:
        raise ValueError(ERR_EMPTY_LIST_TEMPL.format('Стоимости'))
    if len(weights) != len(costs):
        raise ValueError(ERR_LENGTHS_NOT_EQUAL)
    if not all(isinstance(w, int) for w in weights):
        raise TypeError(ERR_NOT_INT_TEMPL.format('Веса'))
    if not all(isinstance(c, int) for c in costs):
        raise TypeError(ERR_NOT_INT_TEMPL.format('Стоимости'))
    if any(w <= 0 for w in weights):
        raise ValueError(ERR_NOT_POS_TEMPL.format('Веса'))
    if any(c <= 0 for c in costs):
        raise ValueError(ERR_NOT_POS_TEMPL.format('Стоимости'))
    if not isinstance(weight_limit, int):
        raise TypeError(ERR_NOT_INT_WEIGHT_LIMIT)
    if weight_limit < 1:
        raise ValueError(ERR_NOT_POS_WEIGHT_LIMIT)
    if weight_limit < min(weights):
        raise ValueError(ERR_LESS_WEIGHT_LIMIT)
    if len(weights) > max_items:
        raise ValueError(f'Количество предметов превышает {max_items}')

    n = len(weights)
    max_cost = 0
    best_combination = []

    def generate_combinations(arr):
        result = [[]]
        for item in arr:
            new_combinations = [current + [item] for current in result]
            result.extend(new_combinations)
        return result

    all_combinations = generate_combinations(list(range(n)))

    for combination in all_combinations:
        current_weight = sum(weights[i] for i in combination)
        if current_weight <= weight_limit:
            current_cost = sum(costs[i] for i in combination)
            if current_cost > max_cost:
                max_cost = current_cost
                best_combination = combination

    return {COST: max_cost, ITEMS: best_combination}


if __name__ == '__main__':
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print('Пример решения задачи о рюкзаке\n')
    print(f'Веса предметов для комплектования рюкзака: {weights}')
    print(f'Стоимости предметов для комплектования рюкзака: {costs}')
    print(f'Ограничение вместимости рюкзака: {weight_limit}')
    result = get_knapsack(weights, costs, weight_limit)
    print(f'Максимальная стоимость: {result[COST]}, '
          f'индексы предметов: {result[ITEMS]}')
