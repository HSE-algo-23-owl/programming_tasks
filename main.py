from typing import Any


def generate_permutations(items: frozenset[Any]) -> list[list[Any]]:
    """Генерирует все варианты перестановок элементов указанного множества
    :param items: неизменяемое множество элементов
    :raise TypeError: если параметр items не является неизменяемым множеством
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """
    __validate(items)
    items_set = set(item for item in items)

    return sorted(__generate_permutations_rec(items_set))


def __generate_permutations_rec(items_set: set[Any]) -> list[list[Any]]:
    """Вспомогательная функция для генерации перестановок элементов методом рекурсии
    :param items_set: изменяемое множество элементов
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """
    if len(items_set) < 1:
        return []
    if len(items_set) == 1:
        return [[items_set.pop()]]

    current_item = items_set.pop()
    permutations_list = __generate_permutations_rec(items_set)

    pmt_lst_help = []  # вспомогательный список для хранения сгенерированных перестановок
    for pmt in permutations_list:  # проход по всем вложенным спискам
        pmt.append(current_item)   # добавление текущего элемента в каждый вложенный список

        pmt_lst_help.append(pmt)
        for pos in range(len(pmt) - 1):
            pmt_help = [item for item in pmt]  # вспомогательный список для осущствления перестановки
            pmt_help[-1], pmt_help[pos] = pmt_help[pos], pmt_help[-1]  # создание перестановки из нового элемента и существующего
            pmt_lst_help.append(pmt_help)  # добавление сгенерированной перестановки в общий вспомогательный список

    return pmt_lst_help


def __validate(items: Any) -> None:
    """Вспомогательная функция для валидации данных
    :param items: любой тип данных
    :raise TypeError: если множество неизменяемое
    """
    if type(items) != frozenset:
        raise TypeError('Параметр items не является неизменяемым множеством')


def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))


if __name__ == '__main__':
    main()