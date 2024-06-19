from typing import TypeVar

T = TypeVar('T')


class HeapSort:
    """Класс, реализующий пирамидальную сортировку."""
    @classmethod
    def __create_heap(cls, data_list: list[T]) -> None:
        """Создает бинарную кучу "на месте" методом перестановки элементов.

        :param data_list: Список элементов.
        """
        length = len(data_list)
        for idx in range(length // 2 - 1, -1, -1):
            cls.__sift_down(data_list, length, idx)

    @classmethod
    def __sift_down(cls, data_list: list[T], length: int, idx: int) -> None:
        """Просеивает минимальные элементы вниз, поддерживает свойство кучи.

        :param data_list: Список элементов.
        :param length: Длина списка.
        :param length: Индекс текущего элемента.
        """
        left_idx = 2 * idx + 1
        right_idx = 2 * idx + 2

        max_idx = left_idx

        if left_idx >= length:
            return
        try:
            if right_idx < length and data_list[max_idx] < data_list[right_idx]:
                max_idx = right_idx

            if data_list[idx] < data_list[max_idx]:
                data_list[idx], data_list[max_idx] = data_list[max_idx], data_list[idx]
                cls.__sift_down(data_list, length, max_idx)
        except TypeError as e:
            raise TypeError(
                    f"'<' not supported between instances of '{type(data_list[max_idx]).__name__}' and '{type(data_list[idx]).__name__}'")

    @classmethod
    def sort(cls, data_list: list[T]) -> None:
        """Сортирует элементы списка..

        :param data_list: Список элементов.
        """
        cls.__create_heap(data_list)

        length = len(data_list)
        for i in range(1, length):
            data_list[0], data_list[length-i] = data_list[length-i], data_list[0]
            cls.__sift_down(data_list, length-i, 0)


def main():
    lst = [5, 8, 1, 4, -7, 6, 12, 19, -6]
    HeapSort().sort(lst)
    print(lst)


if __name__ == '__main__':
    main()
