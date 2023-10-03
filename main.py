import time

def __is_suitable_gcd_values(n1, n2):
    if type(n1) != int:
        raise Exception('Значение параметра a не является целым числом')
    if type(n2) != int:
        raise Exception('Значение параметра b не является целым числом')
    if n1 == 0 and n2 == 0:
        raise Exception('Значения параметров a и b равны нулю')


def __is_suitable_lcm_values(n1, n2):
    if type(n1) != int or n1 < 1:
        raise Exception('Значение параметра a не является натуральным '
                       'положительным числом')
    if type(n2) != int or n2 < 1:
        raise Exception('Значение параметра b не является натуральным '
                       'положительным числом')


def gcd_recursive(n1: int, n2: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Рекурсивная реализация
    """
    __is_suitable_gcd_values(n1, n2)
    n1 = abs(n1)
    n2 = abs(n2)
    if n1 == 0:
        return n2
    elif n2 == 0:
        return n1
    else:
        return gcd_recursive(n2, n1 % n2)


def gcd_iterative_slow(n1: int, n2: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Медленная итеративная реализация
    """
    __is_suitable_gcd_values(n1, n2)
    n1 = abs(n1)
    n2 = abs(n2)
    while True:
        if n1 == 0 or n2 == 0:
            return max(n1, n2)
        if n1 >= n2:
            n1 -= n2
        else:
            n2 -= n1


def gcd_iterative_fast(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Быстрая итеративная реализация
    """
    __is_suitable_gcd_values(a, b)
    a = abs(a)
    b = abs(b)
    while True:
        if a == 0 or b == 0:
            return max(a, b)
        if a > b:
            a %= b
        else:
            b %= a


def lcm(n1: int, n2: int) -> int:
    """Вычисляет наименьшее общее кратное двух натуральных чисел
    """
    __is_suitable_lcm_values(n1, n2)
    n1 = abs(n1)
    n2 = abs(n2)
    return int((n1 * n2) / gcd_iterative_fast(n1, n2))


def main():
    a = 1005002
    b = 1354
    print(f'Вычисление НОД чисел {a} и {b} рекурсивно:')
    start_time = time.time()
    print(gcd_recursive(a, b))
    print(f'Продолжительность: {time.time() - start_time} сек')

    print(f'\nВычисление НОД чисел {a} и {b} итеративно с вычитанием:')
    start_time = time.time()
    print(gcd_iterative_slow(a, b))
    print(f'Продолжительность: {time.time() - start_time} сек')

    print(f'\nВычисление НОД чисел {a} и {b} итеративно с делением:')
    start_time = time.time()
    print(gcd_iterative_fast(a, b))
    print(f'Продолжительность: {time.time() - start_time} сек')

    print(f'\nВычисление НОК чисел {a} и {b}:')
    start_time = time.time()
    print(lcm(a, b))
    print(f'Продолжительность: {time.time() - start_time} сек')


if __name__ == '__main__':
    main()
