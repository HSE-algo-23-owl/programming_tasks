from typing import Any


def generate_permutations(elements: frozenset[Any]) -> list[Any]:
    """Генерирует все варианты перестановок элементов указанного множества
    :param elements: неизменяемое множество элементов
    :raise TypeError: если параметр items не является неизменяемым множеством
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """
    validate(elements)
    return rec_permut_find(list(elements))

def validate(items: frozenset[Any]):
    if type(items) != frozenset:
        raise TypeError("Параметр items не является неизменяемым множеством")

def rec_permut_find(elements: list[Any]):
    if len(elements) == 1:
        return [elements]
    result = []
    for i in range(len(elements)):
        current = elements[i]
        leftover = elements[:i] + elements[i + 1:]
        for permutation in rec_permut_find(leftover):
            result.append([current] + permutation)
    return result

def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))


if __name__ == '__main__':
    main()
