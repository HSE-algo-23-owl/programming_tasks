from knapsack_problem.constants import ERR_LENGTHS_NOT_EQUAL, \
    ERR_NOT_INT_WEIGHT_LIMIT, ERR_NOT_POS_WEIGHT_LIMIT, ERR_LESS_WEIGHT_LIMIT, \
    ERR_NOT_LIST_TEMPL, ERR_EMPTY_LIST_TEMPL, ERR_NOT_INT_TEMPL, \
    ERR_NOT_POS_TEMPL, WEIGHTS, COSTS


def validate_params(weights: list[int], costs: list[int],
                    weight_limit: int) -> None:
    """Проверяет входные данные задачи о рюкзаке.

        :param weights: Список весов предметов для рюкзака.
        :param costs: Список стоимостей предметов для рюкзака.
        :param weight_limit: Ограничение вместимости рюкзака.
        :raise TypeError: Если веса или стоимости не являются списком с числовыми
        значениями, если ограничение вместимости не является целым числом.
        :raise ValueError: Если в списках присутствует нулевое или отрицательное
        значение.
    """
    __check_list_raises_ex(weights, WEIGHTS)
    __check_list_raises_ex(costs, COSTS)
    if len(weights) != len(costs):
        raise ValueError(ERR_LENGTHS_NOT_EQUAL)
    if not isinstance(weight_limit, int):
        raise TypeError(ERR_NOT_INT_WEIGHT_LIMIT)
    if weight_limit < 1:
        raise ValueError(ERR_NOT_POS_WEIGHT_LIMIT)
    if weight_limit < min(weights):
        raise ValueError(ERR_LESS_WEIGHT_LIMIT)


def __check_list_raises_ex(items: list[int], list_name: str) -> None:
    if not isinstance(items, list):
        raise TypeError(ERR_NOT_LIST_TEMPL.format(list_name))
    if len(items) == 0:
        raise ValueError(ERR_EMPTY_LIST_TEMPL.format(list_name))
    for item in items:
        if not isinstance(item, int):
            raise TypeError(ERR_NOT_INT_TEMPL.format(list_name))
        if item < 1:
            raise ValueError(ERR_NOT_POS_TEMPL.format(list_name))
