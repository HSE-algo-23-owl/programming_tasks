from __future__ import annotations

import random
from typing import Callable, TypeVar

STAGE = 0
WIN = 1
LOOS = 2
T = TypeVar('T')

def check_Exseptions(sample, get_winner):
    if not isinstance(sample, (list, tuple)):
        raise TypeError("Sample for a tournament is not a list or a tuple")
    if len(sample) <= 1:
        raise ValueError("Sample for the tournament consists of less than two objects")
    if get_winner is None or not callable(get_winner):
        raise TypeError("get_winner is not a function")
    result = get_winner(sample[0], sample[1])
    if result not in sample:
        raise RuntimeError("get_winner function returned an invalid value")
def tournament(sample: list[T] | tuple[T], get_winner: Callable[[T, T], T]):
    """Выполняет турнирный отбор из заданной выборки. Проводит серию турниров
    между парами объектов из выборки. Победители каждого турнира переходят на
    следующий этап, пока не останется один победитель.

    :param sample: Выборка для проведения турнира.
    :param get_winner: Функция для выбора победителя из двух объектов.
    :raises TypeError: Если выборка объектов не является списком или кортежем
    или функция выбора победителя имеет некорректный тип.
    :raises ValueError: Если выборка объектов пуста.
    :raises RuntimeError: Если функция get_winner возвращает некорректное
    значение.
    :return: Объект победитель турнира.
    """
    check_Exseptions(sample,get_winner)
    if isinstance(sample, (tuple)):
        sample = list(sample)
    i=1
    while i< len(sample):
        if get_winner(sample[i],sample[i-1]) == sample[i-1]:
            sample.append(sample[i-1])
        else:
            sample.append(sample[i])
        i+=2

    return sample[-1]

if __name__ == '__main__':
    sample = [(1, 2)]
    random.shuffle(sample)

    print(f'Список: {sample}')
    print(f'Победитель турнира: {tournament(sample, lambda x, y: max(x, y))}')
