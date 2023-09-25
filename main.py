import time


def fibonacci_rec(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована рекурсивно.
        1  1  2 3 5
    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if type(n) != int or n < 1:
        raise Exception("Ошибка! Функция принимает только целые положительные числа")

    if n in (1, 2):
        return 1

    return fibonacci_rec(n-2) + fibonacci_rec(n-1)


def fibonacci_iter(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if type(n) != int or n < 1:
        raise Exception("Ошибка! Функция принимает только целые положительные числа")

    first = second = 1
    for _ in range(3, n+1):
        first, second = second, first + second

    return second



def rabbits(month: int, lifetime: int) -> int:
    """Возвращает количество пар кроликов в популяции на заданный месяц.
    В начальный момент времени имеется одна пара кроликов. Начиная со второго
    месяца после рождения кролики производят новую пару кроликов каждый месяц.
    После достижения предельного возраста кролики умирают.

    :param month: количество месяцев жизни популяции
    :param lifetime: продолжительность жизни кролика, не менее 2 месяцев
    :return: количество пар кроликов
    """
    pass
    # if month < 2:
    #     return 1
    #
    # previousMonth = currentMonth = 1
    # for i in range(2, month+1):
    #     previousMonth, currentMonth = currentMonth, previousMonth + currentMonth
    #
    #     if i >= lifetime:
    #         currentMonth -= previousMonth
    #
    # return currentMonth



def main():
    n = 35
    print(f'Вычисление {n} числа Фибоначчи рекурсивно:')
    start_time = time.time()
    print(fibonacci_rec(n))
    print(f'duration: {time.time() - start_time} seconds')

    print(f'\nВычисление {n} числа Фибоначчи итеративно:')
    start_time = time.time()
    print(fibonacci_iter(n))
    print(f'duration: {time.time() - start_time} seconds')

    if rabbits(1, 2):
        lifetime = 5
        print(f'\nВычисление числа пар кроликов по состоянию на {n} месяц')
        print(f'при продолжительности жизни кролика {lifetime} месяцев')
        print(rabbits(n, lifetime))


if __name__ == '__main__':
    #main()
    print(rabbits(4, 8))
