COST = 'cost'
ITEMS = 'items'
WEIGHTS = 'Веса'
COSTS = 'Стоимости'
ERR_LENGTHS_NOT_EQUAL = 'Списки весов и стоимости разной длины'
ERR_NOT_INT_WEIGHT_LIMIT = 'Ограничение вместимости рюкзака не является целым числом'
ERR_NOT_POS_WEIGHT_LIMIT = 'Ограничение вместимости рюкзака меньше единицы'
ERR_LESS_WEIGHT_LIMIT = 'Ограничение вместимости рюкзака меньше чем минимальный вес предмета'
ERR_NOT_LIST_TEMPL = '{0} не являются списком'
ERR_EMPTY_LIST_TEMPL = '{0} являются пустым списком'
ERR_NOT_INT_TEMPL = '{0} содержат не числовое значение'
ERR_NOT_POS_TEMPL = '{0} содержат нулевое или отрицательное значение'
MAX_ITEMS = 20
ERR_TOO_MANY_ITEMS = "Количество предметов не должно превышать 21"


def validate_input(weights: list[int], costs: list[int], weight_limit: int):
    if not isinstance(weights, list):
        raise TypeError(ERR_NOT_LIST_TEMPL.format(WEIGHTS))
    if not isinstance(costs, list):
        raise TypeError(ERR_NOT_LIST_TEMPL.format(COSTS))
    if not weights:
        raise ValueError(ERR_EMPTY_LIST_TEMPL.format(WEIGHTS))
    if not costs:
        raise ValueError(ERR_EMPTY_LIST_TEMPL.format(COSTS))
    if any(type(item) is not int for item in weights):
        raise TypeError(ERR_NOT_INT_TEMPL.format(WEIGHTS))
    if any(type(item) is not int for item in costs):
        raise TypeError(ERR_NOT_INT_TEMPL.format(COSTS))
    if any(item <= 0 for item in weights):
        raise ValueError(ERR_NOT_POS_TEMPL.format(WEIGHTS))
    if any(item <= 0 for item in costs):
        raise ValueError(ERR_NOT_POS_TEMPL.format(COSTS))
    if len(weights) != len(costs):
        raise ValueError(ERR_LENGTHS_NOT_EQUAL)
    if not isinstance(weight_limit, int):
        raise TypeError(ERR_NOT_INT_WEIGHT_LIMIT)
    if weight_limit <= 0:
        raise ValueError(ERR_NOT_POS_WEIGHT_LIMIT)
    if any(item > weight_limit for item in weights):
        raise ValueError(ERR_LESS_WEIGHT_LIMIT)
    if len(weights) > MAX_ITEMS:
        raise ValueError(ERR_TOO_MANY_ITEMS)


def get_knapsack(weights: list[int], costs: list[int], weight_limit: int) -> \
        dict[str, int | list[int]]:
    """Решает задачу о рюкзаке с использованием полного перебора.
    :param weights: Список весов предметов для рюкзака.
    :param costs: Список стоимостей предметов для рюкзака.
    :param weight_limit: Ограничение вместимости рюкзака.
    :raise TypeError: Если веса или стоимости не являются списком с числовыми
    значениями, если ограничение вместимости не является целым числом.
    :raise ValueError: Если в списках присутствует нулевое или отрицательное
    значение, если количество предметов превышает 20.
    :return: Словарь с ключами: cost - максимальная стоимость предметов в
    рюкзаке, items - список с индексами предметов, обеспечивающих максимальную
    стоимость.
    """
    validate_input(weights, costs, weight_limit)
    optimal_cost = 0
    optimal_combination = []
    for combination_index in range(1, 2 ** len(weights)):
        current_combination = [i for i in range(len(weights)) if combination_index & (1 << i)]
        if sum(weights[i] for i in current_combination) <= weight_limit:
            current_cost = sum(costs[i] for i in current_combination)
            if current_cost > optimal_cost:
                optimal_cost = current_cost
                optimal_combination = current_combination
    return {COST: optimal_cost, ITEMS: optimal_combination}


if __name__ == '__main__':
    weights = [11, 4, 8, 6, 3, 5, 5, 222]  # Добавлен большой элемент для проверки ограничения
    costs = [17, 6, 11, 10, 5, 8, 6, 30]  # Соответствующая стоимость большого элемента
    weight_limit = 30
    try:
        print('Пример решения задачи о рюкзаке\n')
        print(f'Веса предметов для комплектования рюкзака: {weights}')
        print(f'Стоимости предметов для комплектования рюкзака: {costs}')
        print(f'Ограничение вместимости рюкзака: {weight_limit}')
        result = get_knapsack(weights, costs, weight_limit)
        print(f'Максимальная стоимость: {result[COST]}, '
              f'индексы предметов: {result[ITEMS]}')
    except ValueError as e:
        print(f"Ошибка: {e}")

