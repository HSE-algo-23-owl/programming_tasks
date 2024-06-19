import unittest
from final_task.AlgoWizards.main import HeapSort

ERR_INCOMPARABLE_EMBEDDED_TYPES = "'<' not supported between instances of '{}' and '{}'"


class HeapTest(unittest.TestCase):
    """Класс для тестирования сортировки бинарной кучей"""

    def test_empty_list(self):
        """Проверяет сортировку пустого списка"""
        lst = []
        HeapSort.sort(lst)
        self.assertEqual(lst, [])

    def test_single_element_list(self):
        """Проверяет сортировку списка с одним элементом"""
        lst = [8]
        HeapSort.sort(lst)
        self.assertEqual(lst, [8])

    def test_identical_elements_list(self):
        """Проверяет сортировку списка с одинаковыми элементами"""
        lst = [5, 5, 5, 5, 5, 5]
        HeapSort.sort(lst)
        self.assertEqual(lst, [5, 5, 5, 5, 5, 5])

    def test_repeated_elements_list(self):
        """Проверяет сортировку списка с повторяющимися элементами"""
        lst = [9, 12, 4, -3, -5, 7, -5, 6, 6, 1, -10, -5]
        HeapSort.sort(lst)
        self.assertEqual(lst, [-10, -5, -5, -5, -3, 1, 4, 6, 6, 7, 9, 12])

    def test_unique_elements_list(self):
        """Проверяет сортировку списка с уникальными элементами"""
        lst = [5, 4, -2, 8, 0, -3, -5, 10, 1, -4, 7, -1, 6, 9, 2, 3]
        HeapSort.sort(lst)
        self.assertEqual(lst,[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_mixed_int_float_list(self):
        """Проверяет сортировку списка с вещественными и целыми числами"""
        lst = [3, 9, 1.4, -2.7, 10.23, 7.77]
        HeapSort.sort(lst)
        self.assertEqual(lst, [-2.7, 1.4, 3, 7.77, 9, 10.23])

    def test_string_list(self):
        """Проверяет сортировку списка строк"""
        lst = ["кот", "котенок", "ab", "котик", "a", "aa"]
        HeapSort.sort(lst)
        self.assertEqual(lst, ['a', 'aa', 'ab', 'кот', 'котенок', 'котик'])

    def test_ascending_sorted_list(self):
        """Проверяет сортировку отсортированного по возрастанию списка"""
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        HeapSort.sort(lst)
        self.assertEqual(lst, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_descending_sorted_list(self):
        """Проверяет сортировку отсортированного по убыванию списка"""
        lst = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        HeapSort.sort(lst)
        self.assertEqual(lst, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_user_objects_list(self):
        """Проверяет сортировку пользовательских объектов"""
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y

            def __eq__(self, other):
                return self.x == other.x and self.y == other.y

            def __lt__(self, other):
                return self.x < other.x

            def __gt__(self, other):
                return self.x > other.x

            def __le__(self, other):
                return self.x <= other.x

            def __ge__(self, other):
                return self.x >= other.x

            def __repr__(self):
                return f"Point({self.x}, {self.y})"

        lst = [Point(2,3), Point(7, 7), Point(4,4), Point(10, 6)]
        HeapSort.sort(lst)

        self.assertEqual(lst,[Point(2,3), Point(4,4), Point(7, 7), Point(10, 6)])

    def test_incomparable_embedded_types(self):
        """Проверяет выброс исключения при попытке сравнения несравниваемых типов"""
        with self.assertRaises(TypeError) as err:
            HeapSort.sort([1, 'a'])
        self.assertEqual(ERR_INCOMPARABLE_EMBEDDED_TYPES.format('str', 'int'), str(err.exception))

    def test_incomparable_user_types(self):
        """Проверяет выброс исключение при попытке сравнения несравниваемых пользовательских объектов"""
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        with self.assertRaises(TypeError) as err:
            HeapSort.sort([Point(1,1), Point(7,7)])
        self.assertEqual(ERR_INCOMPARABLE_EMBEDDED_TYPES.format('Point', 'Point'), str(err.exception))


if __name__ == '__main__':
    unittest.main()