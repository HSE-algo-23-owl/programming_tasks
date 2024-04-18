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
    if not isinstance(sample, (list, tuple)):
        raise TypeError("Sample for a tournament is not a list or a tuple")
    if not callable(get_winner):
        raise TypeError("get_winner is not a function")
    if len(sample) < 2:
        raise ValueError("Sample for the tournament consists of less than two objects")

    while len(sample) > 1:
        next_round = []
        for i in range(0, len(sample), 2):
            if i + 1 < len(sample):
                winner = get_winner(sample[i], sample[i + 1])
                if winner not in (sample[i], sample[i + 1]):
                    raise RuntimeError("get_winner function returned an invalid value")
                next_round.append(winner)
            else:
                next_round.append(sample[i])
        sample = next_round

    return sample[0]


if __name__ == '__main__':
    sample = [i for i in range(21)]
    random.shuffle(sample)
    print(f'Список: {sample}')
    print(f'Победитель турнира: {tournament(sample, lambda x, y: max(x, y))}')
