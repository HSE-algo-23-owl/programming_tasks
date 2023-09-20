import time


def check_number(n):
    """Проверяем число на входе"""
    if type(n) != int:
        print("Нужно ввести натурально число вообще-то....")
    elif n < 1:
        print("Наша программа выводит только положительные числа Фибоначчи")
    else:
        return True


def fibonacci_rec(n):
    """Возвращает N-е число Фибоначчи. Реализована рекурсивно.
    :param n: Порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if check_number(n):
        if n == 1 or n == 2:
            return 1
        return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)
    pass

'''я люблю питонапролдж'''
def fibonacci_iter(n):
    """Возвращает N-е число Фибоначчи. Реализована итеративно.
    :param n: Порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if check_number(n):
        if n == 1 or n == 2:
            return 1
        numbers_arr = [1] * n
        for i in range(2, n):
            numbers_arr[i] = numbers_arr[i - 1] + numbers_arr[i - 2]
        return numbers_arr[-1]
    pass


def main():
    n = int(input("Введите порядковый номер числа Фибоначчи - "))
    print(f'Вычисление {n} числа Фибоначчи рекурсивно:')
    start_time = time.time()
    print(fibonacci_rec(n))
    print(f'duration: {time.time() - start_time} seconds')

    print(f'\nВычисление {n} числа Фибоначчи итеративно:')
    start_time = time.time()
    print(fibonacci_iter(n))
    print(f'duration: {time.time() - start_time} seconds')



if __name__ == '__main__':
    main()
