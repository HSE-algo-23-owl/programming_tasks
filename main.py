from typing import Any


def check_gen_rec(items):
    if type(items) != frozenset:
        raise TypeError("Параметр items не является неизменяемым множеством")


def generate_permutations(items: frozenset[Any]) -> list[Any]:
    """Генерирует все варианты перестановок элементов указанного множества
    :param items: неизменяемое множество элементов
    :raise TypeError: если параметр items не является неизменяемым множеством
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """
    check_gen_rec(items)
    mylist = list(items)
    # for perm in helper(mylist): ## выводит в столбик
    #     print(perm)
    return helper(mylist)


def helper(lst):
    if len(lst) == 0:
        return []
    elif len(lst) == 1:
        return [lst]
    else:
        l = []
        for i in range(len(lst)):
            cur_elem = lst[i]
            rest = lst[:i] + lst[i + 1:]
            for perm in helper(rest):
                l.append([cur_elem] + perm)
        return l


def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))


if __name__ == '__main__':
    main()

