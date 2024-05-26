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
ERR_LEN = "Количество предметов превышает лимит - 21 предметов в рюкзаке"
def is_list(list_to_check, name):
    if not isinstance(list_to_check, list):
        raise TypeError(ERR_NOT_LIST_TEMPL.format(name))
    if not all(isinstance(element, int) for element in list_to_check):
        raise TypeError(ERR_NOT_INT_TEMPL.format(name))
    if len(list_to_check) == 0:
        raise ValueError(ERR_EMPTY_LIST_TEMPL.format(name))
    if 0 in list_to_check or any(element < 0 for element in list_to_check):
        raise ValueError(ERR_NOT_POS_TEMPL.format(name))
def validation(weights: list[int], costs: list[int], weight_limit: int) -> None:
    is_list(weights, WEIGHTS)
    is_list(costs, COSTS)
    if len(weights) != len(costs):
        raise ValueError(ERR_LENGTHS_NOT_EQUAL)
    if not isinstance(weight_limit, int):
        raise TypeError(ERR_NOT_INT_WEIGHT_LIMIT)
    if weight_limit == 0 or weight_limit < 0:
        raise ValueError(ERR_NOT_POS_WEIGHT_LIMIT)
    if min(weights) > weight_limit:
        raise ValueError(ERR_LESS_WEIGHT_LIMIT)
    check_len(weights)
def check_len(weight, limit =21):
    if len(weight) > limit:
        raise ValueError(ERR_LEN)

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
    validation(weights,costs,weight_limit)

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


if __name__ == '__main__':
    weights = [11, 4, 8, 6, 3, 5, 5, 8 , 9 ,10, 11, 12, 13 ,14, 15 ,16 , 17, 18 ,19 ,20, 22,22]
    costs = [17, 6, 11, 10, 5, 8, 6, 8 ,9 ,10, 11, 12, 13 ,14, 15, 16 , 71, 18 ,19, 20,22,22 ]
    weight_limit = 30
    get_knapsack(weights, costs, weight_limit)
    print('Пример решения задачи о рюкзаке\n')
    print(f'Веса предметов для комплектования рюкзака: {weights}')
    print(f'Стоимости предметов для комплектования рюкзака: {costs}')
    print(f'Ограничение вместимости рюкзака: {weight_limit}')
    result = get_knapsack(weights, costs, weight_limit)
    print(f'Максимальная стоимость: {result[COST]}, '
          f'индексы предметов: {result[ITEMS]}')
