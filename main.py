from typing import Any


def generate_permutations(items: frozenset[Any]) -> list[Any]:
    """Генерирует все варианты перестановок элементов указанного множества
    :param items: неизменяемое множество элементов
    :raise TypeError: если параметр items не является неизменяемым множеством
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """

    validfrozenset(items)
    return permutations(items)

def permutations(items: frozenset[Any]) -> list[Any]:
    lst = list(items)

    if len(lst) == 0:
        return []

    if len(lst) == 1:
        return [lst]

    carr_elenment = lst.pop(0)

    permut_all_list = permutations(lst)

    permut_all = []

    for elem in permut_all_list:
        for i in range(len(elem) + 1):
            all = elem[0:i] + [carr_elenment] + elem[i:]
            permut_all.append(all)

    return permut_all

# Функция валидации неизменяемого множества элементов
def validfrozenset (items: frozenset[Any]) -> TypeError:
    if type(items) != frozenset:
       raise TypeError("Параметр items не является неизменяемым множеством")

def main():
    items = frozenset((1, 2, 3))
    print(generate_permutations(items))


if __name__ == '__main__':
    main()
