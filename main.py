import time

def fibonacci_rec(n):
    """Возвращает N-е число Фибоначчи. Реализована рекурсивно.
    :param n: Порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n == 1 or n == 2:
        return 1
    return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)



def fibonacci_iter(n):
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



def main():
    while True:
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



if __name__ == '__main__':
    main()
