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
    if type(length) != int:
        raise ValueError(STR_LENGTH_ERROR_MSG)
    if length <= 0:
        raise ValueError(STR_LENGTH_ERROR_MSG)
    strings = []
    generate_zero(length, "", strings)
    generate_one(length, "", strings)
    return strings

def generate_zero (n:int, s:str, strings:list):
    if len(s) + 1 == n:
        strings.append("0" + s)
        return
    generate_one(n, "0" + s, strings)


def generate_one (n:int, s:str, strings:list):
    if len(s) + 1 == n:
        strings.append("1" + s)
        return
    generate_zero(n, "1" + s, strings)
    generate_one(n, "1" + s, strings)


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
        raise ValueError(NOT_INT_VALUE_TEMPL.format("n"))
    if type(k) != int:
        raise ValueError(NOT_INT_VALUE_TEMPL.format("k"))
    if n < 0 :
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("n"))
    if k < 0 :
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("k"))
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)
    if (use_rec):
         return binomial_coefficient_rec(n, k)
    else:
        return binomial_coefficient_iter(n, k)

def binomial_coefficient_rec(n: int, k: int) -> int:
    if k == 0 or n == k:
        return 1
    return binomial_coefficient_rec(n-1, k-1)  + binomial_coefficient_rec(n-1, k)
def binomial_coefficient_iter(n: int, k: int) -> int:
    r = 1
    for i in range(1, k + 1):
        r *= n - k + i
        r //= i
    return r

def main():
    n = 7
    k = 5
    print(binomial_coefficient_iter(n, k))


if __name__ == '__main__':
    main()
