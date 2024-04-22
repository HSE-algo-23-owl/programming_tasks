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
    len_str, consq = input_string.split('\n')
    len_str = int(len_str)
    dupelgager = ""
    for i in range(len_str):
        dupelgager += consq[i]
    ans = []
    minm = dupelgager[0]
    for i in range(0, len_str):
        if dupelgager[i] < minm:
            minm = dupelgager[i]
            ans.append(dupelgager[i:])
        elif dupelgager[i] == minm:
            ans.append(dupelgager[i:])
    ans = sorted(ans)
    return ans[0]


def get_water_volume(input_string: str) -> int:
    """Вычисляет объем воды (количество блоков), который остается после дождя
    на острове.

    :param input_string: Параметры текстом. В первой строке целое число,
    количество столбцов, представляющих ландшафт острова, во второй строке
    список целых чисел, высоты столбцов.
    :return: Целое число, представляющее объем воды (в блоках), который
    останется после дождя.
    """
    amount, height = input_string.split('\n')
    amount = int(amount)
    height = [int(i) for i in height.split()]
    maxm = height[0]
    maxid = 0
    for i in range(amount):
        if height[i] > maxm:
            maxm = height[i]
            maxid = i
    nowmax = height[0]
    water = 0
    for i in range(maxid):
        if nowmax <= height[i]:
            nowmax = height[i]
        water += nowmax - height[i]
    nowmax = height[-1]
    for i in range(amount - 1, maxid, -1):
        if nowmax <= height[i]:
            nowmax = height[i]
        water += nowmax - height[i]
    return water


def main():
    print(get_water_volume('11\n2 5 2 3 6 9 3 1 3 4 6'))

    print(get_win_sequence('4\nMAMA'))  # A
    print(get_win_sequence('4\nALLOALLO'))  # ALLO
    print(get_win_sequence('6\nABCOAXLO'))  # ABCOAX


if __name__ == '__main__':
    main()
