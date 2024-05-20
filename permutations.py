from typing import Any


def generate_permutations(items: frozenset[Any]) -> list[Any]:
    """Генерирует все варианты перестановок элементов указанного множества
    :param items: неизменяемое множество элементов
    :raise TypeError: если параметр items не является неизменяемым множеством
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """
    if items is None or type(items) != frozenset:
        raise TypeError('Параметр items не является неизменяемым множеством')
    set_to_pop = set([item for item in items])
    return __generate_permutations(set_to_pop)


def __generate_permutations(items: set[Any]) -> list[list[Any]]:
    items_cnt = len(items)
    if items_cnt == 0:
        return []
    if items_cnt == 1:
        return [[items.pop()]]
    current = items.pop()
    permutations = __generate_permutations(items)
    new_permutations = []
    for pmt in permutations:
        pmt.append(current)
        for i in range(items_cnt - 1):
            new_pmt = [item for item in pmt]
            new_pmt[i], new_pmt[-1] = new_pmt[-1], new_pmt[i]
            new_permutations.append(new_pmt)
    return permutations + new_permutations


if __name__ == '__main__':
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))
