def get_win_sequence(input_string: str) -> str:
    """Вычисляет минимальную лексикографическую подпоследовательность строки,
    получаемую из исходной строки путем отбрасывания некоторого числа символов
    с начала.

    :param input_string: Параметры текстом. В первой строке целое число, длина
    исходной строки, во второй строке последовательность из заглавных латинских
    букв длинной не менее, заданной первым параметром.
    :return: Строку, представляющую минимальную лексикографическую
    подпоследовательность исходной строки.
    """
    parts = input_string.split('\n')
    n = int(parts[0])
    sequence = parts[1]
    s = ''
    for i in range(n):
        s += sequence[i]
    best_s = ''
    for i in range(n):
        new_s = s[i]
        j = i + 1
        while j < n:
            new_s += s[j]
            j += 1
        if j == n and best_s == '':
            best_s = new_s
        if j == n and best_s != '' and new_s < best_s:
            best_s = new_s
    return best_s

def get_water_volume(input_string: str) -> int:
    """Вычисляет объем воды (количество блоков), который остается после дождя
    на острове.

    :param input_string: Параметры текстом. В первой строке целое число,
    количество столбцов, представляющих ландшафт острова, во второй строке
    список целых чисел, высоты столбцов.
    :return: Целое число, представляющее объем воды (в блоках), который
    останется после дождя.
    """
    parts = input_string.split('\n')
    water = list(map(int, parts[1].split()))
    left, right = 0, len(water) - 1
    max_right = 0
    max_left = 0
    res = 0

    while left < right:
        if water[left] > max_left:
            max_left = water[left]
        if water[right] > max_right:
            max_right = water[right]
        if max_left >= max_right:
            res += max_right - water[right]
            right -= 1
        else:
            res += max_left - water[left]
            left += 1
    return res

def main():
    print(get_water_volume('11\n2 5 2 3 6 9 3 1 3 4 6'))  # 18

    print(get_win_sequence('4\nMAMA'))  # A
    print(get_win_sequence('4\nALLOALLO'))  # ALLO
    print(get_win_sequence('6\nABCOAXLO'))  # ABCOAX


if __name__ == '__main__':
    main()
