import unittest

from main import encode, decode, ERR_NOT_LIST_MSG, ERR_NOT_INT_TEMPL, \
    ERR_EMPTY_LIST_MSG, ERR_NOT_START_WITH_1_MSG, ERR_HAS_DUPLICATES_MSG, \
    ERR_OVER_CONSTRAINT_TEMPL


class TestEncode(unittest.TestCase):
    def test_not_list_numbers(self):
        """Проверяет выброс исключения при передаче некорректного списка."""
        incorrect_values = [None, 1, 'str', {'key': 'val'}]
        for val in incorrect_values:
            with self.assertRaises(TypeError) as error:
                encode(val)
            self.assertEqual(ERR_NOT_LIST_MSG, str(error.exception))

    def test_not_list_val(self):
        """Проверяет выброс исключения при передаче некорректного значения
        в списке."""
        incorrect_lists = [[None], [1.1, 1], ['str', 1, 2],
                           [{'key': 'val'}, 1]]
        for lst in incorrect_lists:
            with self.assertRaises(TypeError) as error:
                encode(lst)
            self.assertEqual(ERR_NOT_INT_TEMPL.format(lst[0]),
                             str(error.exception))

    def test_not_start_with_1(self):
        """Проверяет выброс исключения при передаче списка не начинающегося
        с единицы."""
        with self.assertRaises(ValueError) as error:
            encode([2, 1, 3])
        self.assertEqual(ERR_NOT_START_WITH_1_MSG, str(error.exception))

    def test_has_duplicates(self):
        """Проверяет выброс исключения при передаче списка содержащего
        дубликаты."""
        with self.assertRaises(ValueError) as error:
            encode([1, 2, 3, 2])
        self.assertEqual(ERR_HAS_DUPLICATES_MSG, str(error.exception))

    def test_empty_list(self):
        """Проверяет выброс исключения при передаче пустого списка."""
        with self.assertRaises(ValueError) as error:
            encode([])
        self.assertEqual(ERR_EMPTY_LIST_MSG, str(error.exception))

    def test_1(self):
        """Проверка кодировки 1 элемента."""
        self.assertEqual([1], encode([1]))

    def test_2(self):
        """Проверка кодировки 2 элементов."""
        self.assertEqual([1, 1], encode([1, 2]))

    def test_3(self):
        """Проверка кодировки 3 элементов."""
        self.assertEqual([1, 2, 1], encode([1, 3, 2]))

    def test_4(self):
        """Проверка кодировки 4 элементов."""
        self.assertEqual([1, 2, 1, 1], encode([1, 3, 2, 4]))

    def test_5_asc(self):
        """Проверка кодировки 5 элементов, отсортированных по возрастанию."""
        self.assertEqual([1, 1, 1, 1, 1], encode([1, 2, 3, 4, 5]))

    def test_6_desc(self):
        """Проверка кодировки 6 элементов, отсортированных по убыванию."""
        self.assertEqual([1, 5, 4, 3, 2, 1], encode([1, 6, 5, 4, 3, 2]))

    def test_20(self):
        """Проверка кодировки 20 элементов."""
        natural = [1, 18, 5, 19, 7, 16, 17, 12, 10, 13, 14, 11, 9, 15, 6, 4,
                   20, 8, 2, 3]
        alter = [1, 17, 4, 16, 5, 13, 13, 9, 7, 8, 8, 7, 6, 6, 4, 3, 4, 3, 1,
                 1]
        self.assertEqual(alter, encode(natural))


class TestDecode(unittest.TestCase):
    def test_not_list_numbers(self):
        """Проверяет выброс исключения при передаче некорректного списка."""
        incorrect_values = [None, 1, 'str', {'key': 'val'}]
        for val in incorrect_values:
            with self.assertRaises(TypeError) as error:
                decode(val)
            self.assertEqual(ERR_NOT_LIST_MSG, str(error.exception))

    def test_not_list_val(self):
        """Проверяет выброс исключения при передаче некорректного значения
        в списке."""
        incorrect_lists = [[None], [1.1, 1], ['str', 1, 2],
                           [{'key': 'val'}, 1]]
        for lst in incorrect_lists:
            with self.assertRaises(TypeError) as error:
                decode(lst)
            self.assertEqual(ERR_NOT_INT_TEMPL.format(lst[0]),
                             str(error.exception))

    def test_not_start_with_1(self):
        """Проверяет выброс исключения при передаче списка не начинающегося
        с единицы."""
        with self.assertRaises(ValueError) as error:
            decode([2, 1, 3])
        self.assertEqual(ERR_NOT_START_WITH_1_MSG, str(error.exception))

    def test_empty_list(self):
        """Проверяет выброс исключения при передаче пустого списка."""
        with self.assertRaises(ValueError) as error:
            decode([])
        self.assertEqual(ERR_EMPTY_LIST_MSG, str(error.exception))

    def test_over_constraint(self):
        """Проверяет выброс исключения при передаче пустого списка."""
        with self.assertRaises(ValueError) as error:
            decode([1, 2])
        self.assertEqual(ERR_OVER_CONSTRAINT_TEMPL.format(2, 2), str(error.exception))

    def test_1(self):
        """Проверка декодирования 1 элемента."""
        self.assertEqual([1], decode([1]))

    def test_2(self):
        """Проверка декодирования 2 элементов."""
        self.assertEqual([1, 2], decode([1, 1]))

    def test_3(self):
        """Проверка декодирования 3 элементов."""
        self.assertEqual([1, 3, 2], decode([1, 2, 1]))

    def test_4(self):
        """Проверка декодирования 4 элементов."""
        self.assertEqual([1, 3, 2, 4], decode([1, 2, 1, 1]))

    def test_5_asc(self):
        """Проверка декодирования 5 элементов, отсортированных по возрастанию."""
        self.assertEqual([1, 2, 3, 4, 5], decode([1, 1, 1, 1, 1]))

    def test_6_desc(self):
        """Проверка декодирования 6 элементов, отсортированных по убыванию."""
        self.assertEqual([1, 6, 5, 4, 3, 2], decode([1, 5, 4, 3, 2, 1]))

    def test_20(self):
        """Проверка декодирования 20 элементов."""
        natural = [1, 18, 5, 19, 7, 16, 17, 12, 10, 13, 14, 11, 9, 15, 6, 4,
                   20, 8, 2, 3]
        alter = [1, 17, 4, 16, 5, 13, 13, 9, 7, 8, 8, 7, 6, 6, 4, 3, 4, 3, 1,
                 1]
        self.assertEqual(natural, decode(alter))


if __name__ == '__main__':
    unittest.main()
