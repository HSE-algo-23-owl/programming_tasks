from typing import Any



def generate_permutations(items: frozenset[Any]) -> list[list[Any]]:
    """Генерирует все варианты перестановок элементов указанного множества
    :param items: неизменяемое множество элементов
    :raise TypeError: если параметр items не является неизменяемым множеством
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """
    validate(items)
    if len(items) == 0:
        return []
    items = set([item for item in items])
    return get_permutations_rec(items)

def get_permutations_rec(items):
    # Рекурсия вынесена в отдельную функцию
    if len(items) == 1:
        return [list(items)]
    resultList = []
    for pmt in items:
        remaining_elements = [x for x in items if x != pmt]
        current = get_permutations_rec(remaining_elements)
        for elem in current:
            resultList.append([pmt] + elem)
    return resultList


def validate(items):
    #Проверка на тип данных
   if type(items) != frozenset:
        raise TypeError("Параметр items не является неизменяемым множеством")

def main():
    items = frozenset([1, 2, 3])
    print(generate_permutations(items))

if __name__ == '__main__':
    main()
