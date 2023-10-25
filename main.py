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
    if len(items) == 0: return []
    mylist = list(items)
    result = []
    return helper(mylist, len(items), 0, result)


def helper(elements, n, i, result):
    if i == n:
        result.append(list(elements))
    for j in range(i, n):
        elements[i], elements[j] = elements[j], elements[i]
        helper(elements, n, i + 1, result)
        elements[i], elements[j] = elements[j], elements[i]
    return result


def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))


if __name__ == '__main__':
    main()