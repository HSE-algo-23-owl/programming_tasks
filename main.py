STR_LENGTH_ERROR_MSG = 'Длина строки должна быть целым положительным числом'
"""Сообщение об ошибке при некорректном значении параметра Длина строки"""

NOT_INT_VALUE_TEMPL = 'Параметр {0} Не является целым числом'
"""Шаблон сообщения об ошибке при нечисловом значении параметра"""

NEGATIVE_VALUE_TEMPL = 'Параметр {0} отрицательный'
"""Шаблон сообщения об ошибке при отрицательном значении параметра"""

N_LESS_THAN_K_ERROR_MSG = 'Параметр n меньше чем k'
"""Сообщение об ошибке при значении параметра n меньше чем k"""


def generate_strings(length: int) -> list[str]:
    """Возвращает строки заданной длины, состоящие из 0 и 1, где никакие
    два нуля не стоят рядом.
    :param length: Длина строки.
    :raise ValueError: Если длина строки не является целым положительным
    числом.
    :return: Список строк.
    """
    if type(length) != int or length <= 0:
        raise ValueError(STR_LENGTH_ERROR_MSG)

    s = ''
    lst = []
    if length == 0:
        lst.append(s)
        return lst

    _zero(length, s, lst)
    _one(length, s, lst)
    return lst

def _one(length, s, lst):
    if length == 1:
        lst.append(s + '1')
        return
    _one(length - 1, s + '1', lst)
    _zero(length - 1, s + '1', lst)


def _zero(length, s, lst):
    if length == 1:
        lst.append(s + '0')
        return
    _one(length - 1, s + '0', lst)


def binomial_coefficient(n: int, k: int, use_rec=False) -> int:
    """Вычисляет биномиальный коэффициент из n по k.
    :param n: Количество элементов в множестве, из которого производится выбор.
    :param k: Количество элементов, которые нужно выбрать.
    :param use_rec: Использовать итеративную или рекурсивную реализацию функции.
    :raise ValueError: Если параметры не являются целыми неотрицательными
    числами или значение параметра n меньше чем k.
    :return: Значение биномиального коэффициента.
    """
    if type(n) != int:
        raise ValueError(NOT_INT_VALUE_TEMPL.format('n'))

    if type(k) != int:
        raise ValueError(NOT_INT_VALUE_TEMPL.format('k'))

    validate_binominal_coeff(n, k)

    if use_rec:
        return binomial_coefficient_rec(n, k)
    else:
        return binomial_coefficient_iter(n, k)

def validate_binominal_coeff(n, k):
    if n < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format('n'))

    if k < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format('k'))

    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)

def binomial_coefficient_iter(n: int, k:int):
    с = 1
    for i in range(min(k, n - k)):
        с = с * (n - i) // (i + 1)
    return с

def binomial_coefficient_rec(n: int, k: int):
    if k == n or k == 0:
        return 1
    return binomial_coefficient_rec(n - 1, k - 1) + binomial_coefficient_rec(n - 1, k)

def main():
    n = 3
    print(f'Строки длиной {n}:\n{generate_strings(n)}')

    n = 7
    k = 5
    print(f'Биномиальный коэффициент (итеративно) при n, k ({n}, {k}) = ',
          binomial_coefficient(n, k))
    print(f'Биномиальный коэффициент (рекурсивно) при n, k ({n}, {k}) = ',
          binomial_coefficient(n, k, use_rec=True))


if __name__ == '__main__':
    main()
