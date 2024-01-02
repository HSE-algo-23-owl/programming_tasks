import time


def fibonacci_rec(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована рекурсивно.
    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    match n:
        case 0:
            return 0
        case 1|2:
            return 1
        case _:
            return fibonacci_rec(n - 1 ) + fibonacci_rec(n - 2)


def fibonacci_iter(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    fib_first = 0
    fib_sec = 1
    for __ in range(n):
        fib_first, fib_sec = fib_sec, fib_first + fib_sec
    return fib_first

def rabbits(month: int, lifetime: int) -> int:
    """Возвращает количество пар кроликов в популяции на заданный месяц.
    В начальный момент времени имеется одна пара кроликов. Начиная со второго
    месяца после рождения кролики производят новую пару кроликов каждый месяц.
    После достижения предельного возраста кролики умирают.

    :param month: количество месяцев жизни популяции
    :param lifetime: продолжительность жизни кролика, не менее 2 месяцев
    :return: количество пар кроликов
    """

def rabbits(month: int, lifetime: int) -> int:
    arr_rabbits = []
    for elem in range(month):
        if elem < 2:
            rebbit_two = 1
            arr_rabbits.append(rebbit_two)
        elif (elem < lifetime) or (lifetime == 0):
            rebbit_two = arr_rabbits[elem - 1] + arr_rabbits[elem - 2]
            arr_rabbits.append(rebbit_two)
        elif elem == lifetime:
            rebbit_two = arr_rabbits[elem - 1] + arr_rabbits[elem - 2] - 1
            arr_rabbits.append(rebbit_two)
        else:
            rebbit_two = arr_rabbits[elem - 1] + arr_rabbits[elem - 2] - arr_rabbits[elem - (lifetime + 1)]
            arr_rabbits.append(rebbit_two)
    return rebbit_two


def main():
    n = 8
    print(f'Вычисление {n} числа Фибоначчи рекурсивно:')
    start_time = time.time()
    print(fibonacci_rec(n))
    print(f'duration: {time.time() - start_time} seconds')

    print(f'\nВычисление {n} числа Фибоначчи итеративно:')
    start_time = time.time()
    print(fibonacci_iter(n))
    print(f'duration: {time.time() - start_time} seconds')

    if rabbits(8,5):
        month = 8
        lifetime = 5
        print(f'\nВычисление числа пар кроликов по состоянию на {month} месяц')
        print(f'при продолжительности жизни кролика {lifetime} месяцев')
        print(rabbits(month, lifetime))


if __name__ == '__main__':
    main()

