from typing import Any


def generate_permutations(items: frozenset[Any]) -> list[list[Any]]:
    """Генерирует все варианты перестановок элементов указанного множества
    :param items: неизменяемое множество элементов
    :raise TypeError: если параметр items не является неизменяемым множеством
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """
    __validate(items)
    if len(items) == 0:
        return []
    items = set([item for item in items])
    return get_permutations_rec(items)

def get_permutations_rec(items):
    if len(items) == 1:
        return [[items.pop()]]
    current = items.pop()
    permutations = get_permutations_rec(items)
    output = []
    for pmt in permutations:
        pmt.append(current)
        output.append(pmt)
        for i in range(len(pmt) - 1):
            sub_pmt = [item for item in pmt]
            sub_pmt[-1], sub_pmt[i] = sub_pmt[i], sub_pmt[-1]
            output.append(sub_pmt)
    return output

def __validate(items):
    if type(items) != frozenset:
        raise TypeError('Параметр items не является неизменяемым множеством')
def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))


if __name__ == '__main__':
    main()
