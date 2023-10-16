from typing import Any


def minus_last_elem(x: list[Any]):
    minus_last = generate_permutations(frozenset(x[1:]))
    return minus_last

def generate_permutations(items: frozenset[Any]) -> list[Any]:
    """Генерирует все варианты перестановок элементов указанного множества
    :param items: неизменяемое множество элементов
    :raise TypeError: если параметр items не является неизменяемым множеством
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """
    if type(items) != frozenset:
        raise TypeError('Параметр items не является неизменяемым множеством')
    if len(items) == 0:
        return []
    x = list(items)
    if len(items) == 1:
        return [[x[0]]]
    minus_last = minus_last_elem(x)
    perestanovki = []
    for elem in minus_last:
        for i in range(len(elem) + 1):
            one_perest = elem[:i] + [x[0]] + elem[i:]
            print(elem[:i] + [x[0]] + elem[i:])
            perestanovki.append(one_perest)

    return perestanovki

def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))


if __name__ == '__main__':
    main()
