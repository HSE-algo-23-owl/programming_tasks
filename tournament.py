import random
from typing import Callable, TypeVar

STAGE = 0
WIN = 1
LOOS = 2
T = TypeVar('T')


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
    pass


if __name__ == '__main__':
    sample = [i for i in range(21)]
    random.shuffle(sample)

    print(f'Список: {sample}')
    print(f'Победитель турнира: {tournament(sample, lambda x, y: max(x, y))}')
