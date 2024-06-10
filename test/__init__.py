from knapsack_problem.constants import COST, ITEMS


def check_knapsack_items(weights: list[int], costs: list[int],
                         weight_limit: int,
                         result: dict[str, int | list[int]]) -> bool:
    """Проверяет полученный в результате решения набор предметов для рюкзака."""
    items_cnt = len(weights)
    cost = result[COST]
    items = result[ITEMS]
    if len(items) > items_cnt:
        return False
    if len(items) == 0:
        return False
    sum_cost = 0
    sum_weight = 0
    for idx in items:
        if idx >= items_cnt:
            return False
        sum_cost += costs[idx]
        sum_weight += weights[idx]
    if sum_weight > weight_limit:
        return False
    if sum_cost != cost:
        return False
    return True
