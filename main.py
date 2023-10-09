import time


def check_gcd(a, b):
    if type(a) != int:
        raise Exception("Значение параметра a не является целым числом")
    if type(b) != int:
        raise Exception("Значение параметра b не является целым числом")
    if a == b == 0:
        raise Exception("Значения параметров a и b равны нулю.")


def check_lcm(a, b):
    if type(a) != int or a <= 0:
        raise Exception("Значение параметра a не является натуральным положительным числом")
    if type(b) != int or b <= 0:
        raise Exception("Значение параметра b не является натуральным положительным числом")


def gcd_recursive(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Рекурсивная реализация

    :param a: целое число a
    :param b: целое число b
    :raise Exception: если a или b не являются целыми числами или
    они оба равны нулю
    :return: значение наибольшего общего делителя
    """
    check_gcd(a, b)
    a = abs(a)
    b = abs(b)
    if a * b == 0:
        return a + b
    if a == b :
        return a
    else:
        return gcd_recursive(b, a % b)


def gcd_iterative_slow(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Медленная итеративная реализация

    :param a: целое число a
    :param b: целое число b
    :raise Exception: если a или b не являются целыми числами или
    они оба равны нулю
    :return: значение наибольшего общего делителя
    """
    check_gcd(a, b)
    a = abs(a)
    b = abs(b)
    if a * b == 0:
        return a + b
    if a == b:
        return a
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a


def gcd_iterative_fast(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Быстрая итеративная реализация

    :param a: целое число a
    :param b: целое число b
    :raise Exception: если a или b не являются целыми числами или
    они оба равны нулю
    :return: значение наибольшего общего делителя
    """
    check_gcd(a, b)
    a = abs(a)
    b = abs(b)
    if a * b == 0:
        return a + b
    if a == b :
        return a
    while a % b != 0:
        a, b = b, a % b
    return b


def lcm(a: int, b: int) -> int:
    """Вычисляет наименьшее общее кратное двух натуральных чисел

    :param a: натуральное число a
    :param b: натуральное число b
    :raise Exception: если a или b не являются натуральными числами или
    они равны нулю
    :return: значение наименьшего общего кратного
    """
    check_lcm(a, b)
    a = abs(a)
    b = abs(b)
    return (a*b)/(gcd_iterative_fast(a, b))


def main():
    a = 30
    b = 6
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
