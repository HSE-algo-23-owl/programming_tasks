from tournament import tournament


def main():
    print('Пример использования турнирного отбора')

    sample = [12, 13, 4, 8, 9, 5, 7, 10, 16, 20, 11, 1, 18, 15, 3, 14, 6, 0, 2,
              17, 19]

    print(f'\nСписок: {sample}')
    print('Выбор победителя по максимальному значению числа')
    winner = tournament(sample, lambda x, y: max(x, y))
    print(f'Победитель турнира: {winner}')

    sample = ['В', 'турнире', 'участвуют', 'строки', 'различной', 'длины']
    print(f'\nСписок: {sample}')
    print('Выбор победителя по максимальной длине строки')
    winner = tournament(sample, lambda x, y: x if len(x) > len(y) else y)
    print(f'Победитель турнира: {winner}')


if __name__ == '__main__':
    main()
