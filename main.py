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
    mylist = list(items)
    return helper(mylist)


def helper(items: list[Any]) -> list[Any]:
    if len(items) == 0:
        return []
    elif len(items) == 1:
        return [items]
    else:
        l = []
        for i in range(len(items)):
            curr = items[i]
            rest = items[:i] + items[i+1:]
            for perm in helper(rest):
                l.append([curr] + perm)
        return l


def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))


if __name__ == '__main__':
    main()