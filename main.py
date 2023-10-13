from typing import Any


def __is_suitable_values(items):
    if type(items) != frozenset:
        raise TypeError('Параметр items не является неизменяемым множеством')


def generate_permutations(elements: frozenset[Any]) -> list[Any]:
    """Генерирует все варианты перестановок элементов указанного множества"""
    __is_suitable_values(elements)
    if len(elements) == 0:
        return []
    return __permutations([x for x in elements])


def __permutations(elements):
    if len(elements) == 1:
        return [list(elements)]
    cur = elements.pop()
    res = []
    for elem in __permutations(elements):
        res.append(elem)
        elem.append(cur)
        for j in range(len(elem) - 1):
            swap = [x for x in elem]
            tmp = swap[-1]
            swap[-1] = swap[j]
            swap[j] = tmp
            res.append(swap)
    return res


def main():
    print(generate_permutations(frozenset([1, 2])))


if __name__ == '__main__':
    main()
