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
    __validate_params(sample, get_winner)
    start_idx = 0
    candidate_cnt = len(sample)//2*2
    tour_data = [
        [0]*len(sample),
        [*sample],
        [None]*len(sample),
    ]
    cur_stage = 1
    while candidate_cnt > 1:
        for cur_idx in range(start_idx, start_idx + candidate_cnt - 1, 2):
            tour_data[STAGE].append(cur_stage)
            winner = get_winner(tour_data[WIN][cur_idx],
                                tour_data[WIN][cur_idx + 1])
            if winner not in [tour_data[WIN][cur_idx],
                              tour_data[WIN][cur_idx + 1]]:
                raise RuntimeError('get_winner function returned an invalid '
                                   'value')
            if winner == tour_data[WIN][cur_idx]:
                tour_data[WIN].append(tour_data[WIN][cur_idx])
                tour_data[LOOS].append(tour_data[WIN][cur_idx + 1])
            else:
                tour_data[WIN].append(tour_data[WIN][cur_idx + 1])
                tour_data[LOOS].append(tour_data[WIN][cur_idx])
        cur_stage += 1
        start_idx += candidate_cnt
        candidate_cnt = (len(tour_data[STAGE]) - start_idx) // 2 * 2

    return tour_data[WIN][-1]


def __validate_params(sample: list[T] | tuple[T],
                      get_winner: Callable[[T, T], T]):
    if not isinstance(sample, (list, tuple)):
        raise TypeError('Sample for a tournament is not a list or a tuple')
    if len(sample) < 2:
        raise ValueError('Sample for the tournament consists of less than '
                         'two objects')
    if not isinstance(get_winner, Callable):
        raise TypeError('get_winner is not a function')


if __name__ == '__main__':
    sample = [i for i in range(21)]
    random.shuffle(sample)

    print(f'Список: {sample}')
    print(f'Победитель турнира: {tournament(sample, lambda x, y: max(x, y))}')
