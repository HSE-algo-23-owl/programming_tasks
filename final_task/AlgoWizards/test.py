import unittest


class HeapTest(unittest.TestCase):
    """Класс для тестирования сортировки бинарной кучей"""
    # В качестве заглушки используется метод sorted
    def test_empty_list(self):
        """Проверяет сортировку пустого списка"""
        self.assertEqual(sorted([]), [])

    def test_single_element_list(self):
        """Проверяет сортировку списка с одним элементом"""
        self.assertEqual(sorted([8]), [8])

    def test_identical_elements_list(self):
        """Проверяет сортировку списка с одинаковыми элементами"""
        self.assertEqual(sorted([5, 5, 5, 5, 5, 5]), [5, 5, 5, 5, 5, 5])

    def test_repeated_elements_list(self):
        """Проверяет сортировку списка с повторяющимися элементами"""
        self.assertEqual(sorted([9, 12, 4, -3, -5, 7, -5, 6, 6, 1, -10, -5]),
                         [-10, -5, -5, -5, -3, 1, 4, 6, 6, 7, 9, 12])

    def test_unique_elements_list(self):
        """Проверяет сортировку списка с уникальными элементами"""
        self.assertEqual(sorted([5, 4, -2, 8, 0, -3, -5, 10, 1, -4, 7, -1, 6, 9, 2, 3]),
                         [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_mixed_int_float_list(self):
        """Проверяет сортировку списка с вещественными и целыми числами"""
        self.assertEqual(sorted([3, 9, 1.4, -2.7, 10.23, 7.77]), [-2.7, 1.4, 3, 7.77, 9, 10.23])

    def test_string_list(self):
        """Проверяет сортировку списка строк"""
        self.assertEqual(sorted(["кот", "котенок", "ab", "котик", "a", "aa"]), ['a', 'aa', 'ab', 'кот', 'котенок', 'котик'])

    def test_ascending_sorted_list(self):
        """Проверяет сортировку отсортированного по возрастанию списка"""
        self.assertEqual(sorted([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_descending_sorted_list(self):
        """Проверяет сортировку отсортированного по убыванию списка"""
        self.assertEqual(sorted([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


if __name__ == '__main__':
    unittest.main()