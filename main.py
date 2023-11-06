from typing import Any


def generate_permutations(items: frozenset[Any]) -> list[Any]:
    """Генерирует все варианты перестановок элементов указанного множества
    :param items: неизменяемое множество элементов
    :raise TypeError: если параметр items не является неизменяемым множеством
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """
    validate(items)
    if len(items) == 0:
        return []
    return get_permutations_rec([x for x in items])


def get_permutations_rec(items):
    if len(items) == 1:
        return [[items.pop()]]
    current = items.pop()
    result = []
    permutations = get_permutations_rec(items)
    for pmt in permutations:
        result.append(pmt)
        pmt.append(current)
        for i in range(len(pmt) - 1):
            change = [x for x in pmt]
            change[-1], change[i] = change[i], change[-1]
            result.append(change)
    return result


def validate(items):
    if type(items) != frozenset:
        raise TypeError('Параметр items не является неизменяемым множеством')


def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))


if __name__ == '__main__':
    main()

