PATH_LENGTH_ERROR_MSG = 'Длина маршрута должна быть целым положительным числом'
"""Сообщение об ошибке при некорректном значении параметра Длина маршрута"""

NOT_INT_VALUE_TEMPL = 'Параметр {0} Не является целым числом'
"""Шаблон сообщения об ошибке при нечисловом значении параметра"""

NEGATIVE_VALUE_TEMPL = 'Параметр {0} отрицательный'
"""Шаблон сообщения об ошибке при отрицательном значении параметра"""

N_LESS_THAN_K_ERROR_MSG = 'Параметр n меньше чем k'
"""Сообщение об ошибке при значении параметра n меньше чем k"""


def validation_t_p_c(length: int):
    if type(length) != int or length <= 0:
        raise Exception(PATH_LENGTH_ERROR_MSG)


def a(n):
    if n in [0, 1, 2]:
        return n
    else:
        return b(n - 1) + c(n - 1)


def b(n):
    if n == 1:
        return a(n - 1)
    else:
        return a(n - 1) + c(n - 1)


def c(n):
    if n == 1:
        return a(n - 1)
    else:
        return a(n - 1) + b(n - 1)


def get_triangle_path_count(length: int) -> int:
    if type(length) != int or length <= 0:
        raise ValueError(PATH_LENGTH_ERROR_MSG)
    if length == 1:
        return 0
    else:
        return a(length)


def validation_b_c(n: int, k: int):
    if type(n) != int:
        raise ValueError(NOT_INT_VALUE_TEMPL.format('n'))
    if type(k) != int:
        raise ValueError(NOT_INT_VALUE_TEMPL.format('k'))
    if n < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format('n'))
    if k < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format('k'))
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


def binomial_coefficient_alg_rec(n: int, k: int):
    if k == 0 or k == n:
        return 1
    else:
        return binomial_coefficient(n - 1, k, True) + binomial_coefficient(n - 1, k - 1, True)


def binomial_coefficient_alg_iter(n: int, k: int):
    numerator = 1
    denominator = 1
    for step in range(1, min(k, n - k) + 1):
        numerator *= n
        denominator *= step
        n -= 1
    return numerator // denominator


def binomial_coefficient(n: int, k: int, use_rec=False) -> int:
    validation_b_c(n, k)
    if use_rec:
        return binomial_coefficient_alg_rec(n, k)
    else:
        return binomial_coefficient_alg_iter(n, k)


def main():
    n = 4
    print(f'Количество маршрутов длиной {n} = {get_triangle_path_count(n)}')
    n = 30
    k = 20
    print(f'Биномиальный коэффициент (итеративно) при n, k ({n}, {k}) = ',
          binomial_coefficient(n, k))
    print(f'Биномиальный коэффициент (рекурсивно) при n, k ({n}, {k}) = ',
          binomial_coefficient(n, k, use_rec=True))


if __name__ == '__main__':
    main()
