import time


def fibonacci_rec(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована рекурсивно.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)


def fibonacci_iter(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    fib1 = fib2 = 1
    if n == 1 or n == 2:
        return 1
    for i in range(2, n):
        fib1, fib2 = fib2, fib1 + fib2
    return fib2


def rabbits(month: int, lifetime: int) -> int:
    """
    1 вариант Рекурсивно

    :param month: количество месяцев жизни популяции
    :param lifetime: продолжительность жизни кролика, не менее 2 месяцев
    :return: количество пар кроликов
    """
    if lifetime < month and month > 2:
        return fibonacci_rec(month) - fibonacci_rec(month - lifetime)
    return fibonacci_rec(month)

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
    main()
