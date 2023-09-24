import time


def fibonacci_rec(n: int) -> int:
    if n == 1:
        return 1
    elif n == 0:
        return 0
    else:
        return fibonacci_rec(n-1) + fibonacci_rec(n-2)



def fibonacci_iter(n: int) -> int:
    el1,el2 = 0,1
    if n == 1:
        return 1
    elif n == 0:
        return 0
    for _ in range(1,n):
        el1,el2 = el2,el1 + el2
    return el2



def rabbits(month: int, lifetime: int) -> int:
    if month <= 2:
        return 1
    elif month - lifetime <= 0:
         return rabbits(month-1,lifetime) + rabbits(month-2,lifetime)
    else:
        return rabbits(month-1,lifetime) + rabbits(month-2,lifetime) - rabbits(month - lifetime, lifetime)


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

    if rabbits(1, 2):
        lifetime = 7
        print(f'\nВычисление числа пар кроликов по состоянию на {n} месяц')
        print(f'при продолжительности жизни кролика {lifetime} месяцев')
        print(rabbits(n, lifetime))


if __name__ == '__main__':
    main()
