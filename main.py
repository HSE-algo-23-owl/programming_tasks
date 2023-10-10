from typing import Any


def is_suitable_values(elements):
    if type(elements) != frozenset:
        raise TypeError('Параметр items не является неизменяемым множеством')


def generate_permutations(elements: frozenset[Any]) -> list[Any]:
    """Генерирует все варианты перестановок элементов указанного множества"""
    is_suitable_values(elements)
    if len(elements) == 1:
        return [list(elements)]
    res = []
    for elem in elements:
        tmp = generate_permutations(frozenset([x for x in elements if x != elem]))
        for x in tmp:
            res.append([elem] + list(x))
    return res
    pass


def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))


if __name__ == '__main__':
    main()
