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
def tournament(sample: list[T] | tuple[T], get_winner: Callable[[T, T], T]):

    check_Exseptions(sample,get_winner)
    if isinstance(sample, (tuple)):
        sample = list(sample)
    i=1
    while i < len(sample):
        res = get_winner(sample[i], sample[i-1])
        if res == sample[i-1]:
            sample.append(sample[i-1])
        elif res == sample[i]:
            sample.append(sample[i])
        else:
            raise RuntimeError("get_winner function returned an invalid value")
        i+=2

    return sample[-1]

if __name__ == '__main__':
    sample = [(1, 2)]
    random.shuffle(sample)

    print(f'Список: {sample}')
    print(f'Победитель турнира: {tournament(sample, lambda x, y: max(x, y))}')
