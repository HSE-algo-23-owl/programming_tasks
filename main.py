import time


def validate_1(a, b):
    if type(a) != int:
        raise Exception('Значение параметра a не является целым числом')
    if type(b) != int:
        raise Exception('Значение параметра b не является целым числом')
    if a == 0 and b == 0:
        raise Exception('Значения параметров a и b равны нулю')
def validate_2(a, b):
    if type(a) != int or a <= 0:
        raise Exception('Значение параметра a не является натуральным '
                        'положительным числом')
    if type(b) != int or b <= 0:
        raise Exception('Значение параметра b не является натуральным '
                        'положительным числом')

def gcd_recursive(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Рекурсивная реализация"""
    validate_1(a, b)
    a = abs(a)
    b = abs(b)
    if a == b:
        return a
    if a * b == 0:
        return a + b
    if b > a:
        a, b = b, a
    return gcd_recursive(a - b, b)


def gcd_iterative_slow(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Медленная итеративная реализация"""
    validate_1(a, b)
    a = abs(a)
    b = abs(b)
    if a * b == 0:
        return a + b
    while a != b:
        if b > a:
            a, b = b, a
        a -= b
    return a


def gcd_iterative_fast(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел
    Быстрая итеративная реализация"""
    validate_1(a, b)
    a = abs(a)
    b = abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Вычисляет наименьшее общее кратное двух натуральных чисел"""
    validate_2(a, b)
    a = abs(a)
    b = abs(b)
    return (a * b) // gcd_recursive(a, b)


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

