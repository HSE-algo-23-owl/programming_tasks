from typing import Any


def validate_list(items: frozenset[Any]):
    if type(items) != frozenset:
        raise TypeError('Параметр items не является неизменяемым множеством')


def swap(items, i: int, j: int):
    temp = items[i]
    items[i] = items[j]
    items[j] = temp


def generate_permutations_logic(items: list[Any]) -> list[Any]:
    result = []
    n = len(items)
    if n == 0:
        return result
    indexes = n * [0]
    result.append(items.copy())
    i = 0
    while i < n:
        if indexes[i] < i:
            if i % 2 == 0:
                swap(items, 0, i)
            else:
                swap(items, indexes[i], i)
            result.append(items.copy())
            indexes[i] += 1
            i = 0
        else:
            indexes[i] = 0
            i += 1
    return result


def generate_permutations(items: frozenset[Any]) -> list[Any]:
    validate_list(items)
    items_list = list(items)
    result = generate_permutations_logic(items_list)
    return result


def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))


if __name__ == '__main__':
    main()
