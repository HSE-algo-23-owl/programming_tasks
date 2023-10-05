import time

def __validate_data(a: int, b: int) -> None:
    """Вспомогательная функция для валидации входящих параметров
    :param a: целое число a
    :param b: целое число b
    :raise Exception: если a или b не являются целыми числами или
    они оба равны нулю
    """
    if type(a) != int:
        raise Exception('Значение параметра a не является целым числом')
    if type(b) != int:
        raise Exception('Значение параметра b не является целым числом')
    if a == b == 0:
        raise Exception('Значения параметров a и b равны нулю')


def gcd_recursive(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Рекурсивная реализация

    :param a: целое число a
    :param b: целое число b
    :raise Exception: если a или b не являются целыми числами или
    они оба равны нулю
    :return: значение наибольшего общего делителя
    """
    __validate_data(a, b)
    a, b = abs(a), abs(b)  # если на входе отрицательные числа

    if a == b:  # если числа равны, возвращаем любое из этих чисел
        return a
    if a * b == 0:  # если одно из чисел равно нулю, возвращаем максимальное (сумму)
        return a + b
    if b > a:  # меняем числа местами, если второе число больше первого
        a, b = b, a

    return gcd_recursive(a - b, b)


def gcd_iterative_slow(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Медленная итеративная реализация

    :param a: целое число a
    :param b: целое число b
    :raise Exception: если a или b не являются целыми числами или
    они оба равны нулю
    :return: значение наибольшего общего делителя
    """
    __validate_data(a, b)
    a, b = map(abs, (a, b))

    if a * b == 0:
        return a + b

    while a != b:
        a, b = max(a, b), min(a, b)
        a -= b

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
    __validate_data(a, b)
    a, b = map(abs, (a, b))

    while b:
        a, b = b, a % b

    return a


def lcm(a: int, b: int) -> int:
    """Вычисляет наименьшее общее кратное двух натуральных чисел

    :param a: натуральное число a
    :param b: натуральное число b
    :raise Exception: если a или b не являются натуральными числами или
    они равны нулю
    :return: значение наименьшего общего кратного
    """

    # валидиация данных при помощи генерации словаря и перебора параметров функции - костыль, гораздо логичнее было
    # воспользоваться и пробежаться по коллекции (кортежу) позиционных аргументов args, но тогда бы пришлось менять
    # сигнатуру функции, к тому же была бы нарушена логика задания (функция может принимать только два аргумента)
    params = {param: value for param, value in locals().items()}  # формируем словарь из параметров функции
    for param in params.keys():
        if type(params[param]) != int or params[param] < 1:  # если хотя бы один параметр не
            # является целочисленным числом и меньше единицы
            raise Exception(f"Значение параметра {param} не является натуральным положительным числом")

    return int(a * b / gcd_iterative_fast(a, b))


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

