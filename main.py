import time


def fibonacci_rec(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована рекурсивно.
    :param n: Порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n == 1 or n == 2:
        return 1
    return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)


def fibonacci_iter(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно.
    :param n: Порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n == 1 or n == 2:
        return 1
    numbers_arr = [1] * n
    for i in range(2, n):
        numbers_arr[i] = numbers_arr[i - 1] + numbers_arr[i - 2]
    return numbers_arr[-1]


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


def main():
    while True:
        "Проверка значения на входе"
        try:
            n = int(input("Введите номер числа Фибоначчи - "))
        except ValueError:
            print("Нужно ввести натурально число вообще-то....")
        else:
            if n < 1:
                print("Наша программа выводит только положительные числа Фибоначчи")
                continue
            break

    print(f'Вычисление {n} числа Фибоначчи рекурсивно:')
    start_time = time.time()
    print(fibonacci_rec(int(n)))
    print(f'duration: {time.time() - start_time} seconds')

    print(f'\nВычисление {n} числа Фибоначчи итеративно:')
    start_time = time.time()
    print(fibonacci_iter(int(n)))
    print(f'duration: {time.time() - start_time} seconds')

    if rabbits(1, 2):
        lifetime = 5
        print(f'\nВычисление числа пар кроликов по состоянию на {n} месяц')
        print(f'при продолжительности жизни кролика {lifetime} месяцев')
        print(rabbits(n, lifetime))


if __name__ == '__main__':
    main()
