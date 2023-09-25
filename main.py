import time


def fibonacci_rec(n: int) -> int:
    fib1 = fib2 = 1
    fibres = int
    if (n == 1 or n == 2):
        return 1
    elif (n > 2):
        fibres = fibonacci_rec(n - 1) + fibonacci_rec(n - 2)
    return fibres


def fibonacci_iter(n: int) -> int:
    fib1 = fib2 = 1
    if (n < 3):
        return 1
    for i in range(2, n):
        fib1, fib2 = fib2, fib1 + fib2
    return fib2


def rabbits(month: int, lifetime: int) -> int:
    """Возвращает количество пар кроликов в популяции на заданный месяц.
    В начальный момент времени имеется одна пара кроликов. Начиная со второго
    месяца после рождения кролики производят новую пару кроликов каждый месяц.
    После достижения предельного возраста кролики умирают.

    :param month: количество месяцев жизни популяции
    :param lifetime: продолжительность жизни кролика, не менее 2 месяцев
    :return: количество пар кроликов
    """
    if lifetime > 2 and lifetime < month:
        return fibonacci_rec(month) - fibonacci_rec(month - lifetime)
    return fibonacci_rec(month)


def main():
    n = 10
    print(f'Вычисление {n} числа Фибоначчи рекурсивно:')
    start_time = time.time()
    print(fibonacci_rec(n))
    print(f'duration: {time.time() - start_time} seconds')

    print(f'\nВычисление {n} числа Фибоначчи итеративно:')
    start_time = time.time()
    print(fibonacci_iter(n))
    print(f'duration: {time.time() - start_time} seconds')

    if rabbits(1, 2):
        lifetime = 3
        print(f'\nВычисление числа пар кроликов по состоянию на {n} месяц')
        print(f'при продолжительности жизни кролика {lifetime} месяцев')
        print(rabbits(n, lifetime))


if __name__ == '__main__':
    main()
