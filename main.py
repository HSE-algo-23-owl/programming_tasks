from typing import Any

ERR_NOT_LIST_MSG = 'Переданный параметр не является списком'
ERR_EMPTY_LIST_MSG = 'Переданный список пуст'
ERR_NOT_INT_TEMPL = 'Элемент списка [{0}] не является целым числом'
ERR_NOT_START_WITH_1_MSG = 'Список не начинается с 1'
ERR_HAS_DUPLICATES_MSG = 'Список содержит дубликаты'
ERR_OVER_CONSTRAINT_TEMPL = ('Значение [{0}] в позиции [{1}] превышает '
                             'ограничение n - i + 1')


def __validate_params(lst: Any) -> None:
    """Валидирует переданный список.
            :param lst: Входной параметр. Это может быть любой объект.
            :raise TypeError: Если переданный параметр не является списком целых
            положительных чисел.
            :raise ValueError: Если список содержит дубликаты или не начинается с
            единицы.
            """
    if not isinstance(lst, list):  # проверка на список
        raise TypeError(ERR_NOT_LIST_MSG)
    if not lst:  # проверка на пустоту списка
        raise ValueError(ERR_EMPTY_LIST_MSG)
    for value in lst:  # проверка значений списка
        if not isinstance(value, int):
            raise TypeError(ERR_NOT_INT_TEMPL.format(value))

    if lst[0] != 1:  # проверка 1-го элемента списка
        raise ValueError(ERR_NOT_START_WITH_1_MSG)


def encode(numbers: list[int]) -> list[int]:
    """Переводит решение задачи коммивояжера из натуральной кодировки в
    альтернативную. Решение всегда начинается с единицы.
        :param numbers: Натуральная кодировка решения - список целых
        положительных чисел.
        :raise TypeError: Если переданный параметр не является списком целых
        положительных чисел.
        :raise ValueError: Если список содержит дубликаты или не начинается с
        единицы.
        :return: Альтернативная кодировка решения - список целых
        положительных чисел.
        """
    __validate_params(numbers)
    if len(numbers) > len(set(numbers)):  # проверка на дубликаты
        raise ValueError(ERR_HAS_DUPLICATES_MSG)

    positions = list(range(1, len(numbers) + 1))
    encoding = []

    for number in numbers:
        idx = positions.index(number)
        del positions[idx]
        encoding.append(idx + 1)

    return encoding


def decode(codes: list[int]) -> list[int]:
    """Переводит решение задачи коммивояжера из альтернативной кодировки в
    натуральную.
        :param numbers: Альтернативная кодировка решения - список целых
        положительных чисел.
        :raise TypeError: Если переданный параметр не является списком целых
        положительных чисел.
        :raise ValueError: Если список не начинается с единицы или нарушено
        ограничение (n - i + 1).
        :return: Натуральная кодировка решения - список целых
        положительных чисел.
        """
    __validate_params(codes)
    for pos, value in enumerate(codes, start=1):
        if value > len(codes) - pos + 1:
            raise ValueError(ERR_OVER_CONSTRAINT_TEMPL.format(value, pos))

    positions = list(range(1, len(codes) + 1))
    decoding = []

    for number in codes:
        decoding.append(positions[number-1])
        positions.pop(number-1)

    return decoding


if __name__ == '__main__':
    print('Пример натуральной и альтернативной кодировки решения задачи о '
          'рюкзаке\n')
    natural = [1, 5, 2, 4, 3]
    alter = [1, 1, 1, 2, 1]
    print(f'Натуральный код {natural} -> Альтернативный код {encode(natural)}')
    print(f'Альтернативный код {alter} -> Натуральный код {decode(alter)}')