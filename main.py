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


def get_knapsack(weights: list[int], costs: list[int], lim_weight: int, max_items: int = 25) -> \
        dict[str, int | list[int]]:
    """Решает задачу о рюкзаке с использованием полного перебора.

    :param weights: Список весов предметов для рюкзака.
    :param costs: Список стоимостей предметов для рюкзака.
    :param lim_weight: Ограничение вместимости рюкзака.
    :raise TypeError: Если веса или стоимости не являются списком с числовыми
    значениями, если ограничение вместимости не является целым числом.
    :raise ValueError: Если в списках присутствует нулевое или отрицательное
    значение.
    :return: Словарь с ключами: cost - максимальная стоимость предметов в
    рюкзаке, items - список с индексами предметов, обеспечивающих максимальную
    стоимость.
    """
    def check(var, name):
        if not isinstance(var, list):
            raise TypeError(ERR_NOT_LIST_TEMPL.format(name))
        if not var:
            raise ValueError(ERR_EMPTY_LIST_TEMPL.format(name))
        if not all(isinstance(x, int) for x in var):
            raise TypeError(ERR_NOT_INT_TEMPL.format(name))
        if any(x <= 0 for x in var):
            raise ValueError(ERR_NOT_POS_TEMPL.format(name))

    check(weights, 'Веса')
    check(costs, 'Стоимости')

    if len(weights) != len(costs):
        raise ValueError(ERR_LENGTHS_NOT_EQUAL)
    if not isinstance(lim_weight, int):
        raise TypeError(ERR_NOT_INT_WEIGHT_LIMIT)
    if lim_weight < 1:
        raise ValueError(ERR_NOT_POS_WEIGHT_LIMIT)
    if lim_weight < min(weights):
        raise ValueError(ERR_LESS_WEIGHT_LIMIT)
    if len(weights) > max_items:
        raise ValueError(f'Количество предметов превышает {max_items}')

    res_arr = [[]]
    for item in list(range(len(weights))):
        new_arr = []
        for elem in res_arr:
            new_arr.append(elem + [item])
        res_arr.extend(new_arr)
    maximum = 0
    temp_arr = []
    for elem in res_arr:
        if not(sum(weights[i] for i in elem) > lim_weight):
            if not(sum(costs[i] for i in elem) <= maximum):
                maximum = sum(costs[i] for i in elem)
                temp_arr = elem

    return {COST: maximum, ITEMS: list(temp_arr)}


if __name__ == '__main__':
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    lim_weight = 30
    print('Пример решения задачи о рюкзаке\len(weights)')
    print(f'Веса предметов для комплектования рюкзака: {weights}')
    print(f'Стоимости предметов для комплектования рюкзака: {costs}')
    print(f'Ограничение вместимости рюкзака: {lim_weight}')
    res_arr = get_knapsack(weights, costs, lim_weight)
    print(f'Максимальная стоимость: {res_arr[COST]}, '
          f'индексы предметов: {res_arr[ITEMS]}')
