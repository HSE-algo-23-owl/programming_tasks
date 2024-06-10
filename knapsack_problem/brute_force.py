from knapsack_problem.validate import validate_params
from knapsack_problem.constants import COST, ITEMS


def brute_force(weights: list[int], costs: list[int], weight_limit: int) -> \
        dict[str, int | list[int]]:
    """Решает задачу о рюкзаке с использованием полного перебора.

    :param weights: Список весов предметов для рюкзака.
    :param costs: Список стоимостей предметов для рюкзака.
    :param weight_limit: Ограничение вместимости рюкзака.
    :return: Словарь с ключами: cost - максимальная стоимость предметов в
    рюкзаке, items - список с индексами предметов, обеспечивающих максимальную
    стоимость.
    """
    item_cnt = len(weights)
    if sum(weights) <= weight_limit:
        return {COST: sum(costs),
                ITEMS: [i for i in range(item_cnt)]}
    best_set = 0
    best_cost = 0
    for item_set in range(1, 2**item_cnt):
        cost = 0
        weight = 0
        for idx in range(0, item_cnt):
            cost += costs[idx] if item_set & 2**idx == 2**idx else 0
            weight += weights[idx] if item_set & 2**idx == 2**idx else 0
        if weight <= weight_limit and cost > best_cost:
            best_set = item_set
            best_cost = cost
    items = [idx for idx in range(0, item_cnt) if best_set & 2**idx == 2**idx]
    return {COST: best_cost, ITEMS: items}
