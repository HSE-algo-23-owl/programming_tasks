from typing import Any


def check(items: frozenset[Any]):
    if type(items) != frozenset:
        raise TypeError('Параметр items не является неизменяемым множеством')

def generate_permutations(items: frozenset[Any]) -> list[Any]:
    """Генерирует все варианты перестановок элементов указанного множества
    :param items: неизменяемое множество элементов
    :raise TypeError: если параметр items не является неизменяемым множеством
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """
    check(items)
    return get_permutation(list(items))

def get_permutation(items: frozenset[Any] ):
    if (len(items) == 0):
        return []
    result = list(items)
    if len(items) == 1:
        return [items]
    result = []
    for i in range(len(items)):
        rest = items[:i] + items[i + 1:]
        for p in get_permutation(rest):
            result.append([items[i]] + p)
    return result


def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))


if __name__ == '__main__':
    main()
