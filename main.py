from typing import Any


def validate_list(items: frozenset[Any]):
    if type(items) != frozenset:
        raise TypeError('Параметр items не является неизменяемым множеством')


def swap(items, i: int, j: int):
    temp = items[i]
    items[i] = items[j]
    items[j] = temp


def generate_permutations_logic(items: list[Any], n: int, result: list[Any]) -> list[Any]:
    if n == 1:
        result.append(items.copy())
    else:
        for i in range(n):
            generate_permutations_logic(items, n - 1, result)
            if n % 2 == 0:
                swap(items, i, n - 1)
            else:
                swap(items, 0, n - 1)
    return result


def generate_permutations(items: frozenset[Any]) -> list[Any]:
    validate_list(items)
    items_list = list(items)
    result = []
    result = generate_permutations_logic(items_list, len(items), result)
    return result


def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))


if __name__ == '__main__':
    main()
