import random
import unittest

from tournament import tournament

FUNC_IDX = 0
SAMPLE_IDX = 1
RESULT_IDX = 2
MAX_VALUE = 'MAX_VALUE'
MIN_VALUE = 'MIN_VALUE'
MAX_LEN = 'MAX_LEN'
MIN_LEN = 'MIN_LEN'


class TestTournament(unittest.TestCase):
    test_func = {
        MAX_VALUE: lambda x, y: max(x, y),
        MIN_VALUE: lambda x, y: min(x, y),
        MAX_LEN: lambda x, y: x if len(x) > len(y) else y,
        MIN_LEN: lambda x, y: x if len(x) < len(y) else y
    }

    def test_incorrect_sample(self):
        """Проверка выброса исключения при передаче некорректной выборки
        объектов."""
        incorrect_samples = [None, 1, 1.1, {'key': 'val'}, 'str']
        for sample in incorrect_samples:
            with self.assertRaises(TypeError) as error:
                tournament(sample, self.test_func[MAX_VALUE])
            self.assertEqual(
                'Sample for a tournament is not a list or a tuple',
                str(error.exception))

    def test_empty_sample(self):
        """Проверка выброса исключения при передаче пустой выборки
        объектов."""
        incorrect_samples = [[], ()]
        for sample in incorrect_samples:
            with self.assertRaises(ValueError) as error:
                tournament(sample, self.test_func[MAX_VALUE])
            self.assertEqual('Sample for the tournament consists of less '
                             'than two objects',
                             str(error.exception))

    def test_incorrect_function_type(self):
        """Проверка выброса исключения при передаче функции некорректного
        типа."""
        incorrect_functions = [None, 1, 1.1, {'key': 'val'}, 'str']
        for func in incorrect_functions:
            with self.assertRaises(TypeError) as error:
                tournament([1, 2], func)
            self.assertEqual('get_winner is not a function',
                             str(error.exception))

    def test_incorrect_function(self):
        """Проверка выброса исключения при передаче функции возвращающей
        некорректное значение."""
        with self.assertRaises(RuntimeError) as error:
            tournament([1, 2], lambda x, y: 'incorrect result')
        self.assertEqual('get_winner function returned an invalid value',
                         str(error.exception))

    def test_single(self):
        """Проверка выброса исключения при передаче выборки из одного
        объекта."""
        incorrect_samples = [[1], ('str',)]
        for sample in incorrect_samples:
            with self.assertRaises(ValueError) as error:
                tournament(sample, self.test_func[MAX_VALUE])
            self.assertEqual('Sample for the tournament consists of less '
                             'than two objects',
                             str(error.exception))

    def test_double(self):
        """Проверка выбора турниром из двух участников."""
        test_data = (
            (self.test_func[MAX_VALUE], (1, 2), 2),
            (self.test_func[MAX_VALUE], (1, 1), 1),
            (self.test_func[MIN_VALUE], (1.1, 2.2), 1.1),
            (self.test_func[MIN_VALUE], (1.1, 1.1), 1.1),
            (self.test_func[MAX_VALUE], ('a', 'b'), 'b'),
            (self.test_func[MIN_VALUE], ('a', 'b'), 'a'),
            (self.test_func[MAX_LEN], ('aa', 'b'), 'aa'),
            (self.test_func[MIN_LEN], ('aa', 'b'), 'b'),
        )
        for row in test_data:
            self.assertEqual(tournament(row[SAMPLE_IDX], row[FUNC_IDX]),
                             row[RESULT_IDX])

    def test_triple(self):
        """Проверка выбора турниром из трех участников."""
        test_data = (
            (self.test_func[MAX_VALUE], (1, 2, 3), 3),
            (self.test_func[MAX_VALUE], (1, 1, 1), 1),
            (self.test_func[MIN_VALUE], (1.1, 2.2, 3.), 1.1),
            (self.test_func[MIN_VALUE], (1.1, 1.1, 2), 1.1),
            (self.test_func[MAX_VALUE], ('a', 'b', 'c'), 'c'),
            (self.test_func[MIN_VALUE], ('a', 'b', 'b'), 'a'),
            (self.test_func[MAX_LEN], ('aa', 'b', 'ccc'), 'ccc'),
            (self.test_func[MIN_LEN], ('aa', 'b', 'ccc'), 'b'),
        )
        for row in test_data:
            self.assertEqual(tournament(row[SAMPLE_IDX], row[FUNC_IDX]),
                             row[RESULT_IDX])

    def test_quad(self):
        """Проверка выбора турниром из четырех участников."""
        test_data = (
            (self.test_func[MAX_VALUE], (1, 2, 2, 3), 3),
            (self.test_func[MIN_VALUE], (1.1, 2.2, 3, 4), 1.1),
            (self.test_func[MAX_VALUE], ('a', 'b', 'c', 'aa'), 'c'),
            (self.test_func[MIN_VALUE], ('a', 'b', 'b', 'aa'), 'a'),
            (self.test_func[MAX_LEN], ('aa', 'b', 'ccc', 'aaaa'), 'aaaa'),
            (self.test_func[MIN_LEN], ('aa', 'b', 'ccc', 'aaaa'), 'b'),
        )
        for row in test_data:
            self.assertEqual(tournament(row[SAMPLE_IDX], row[FUNC_IDX]),
                             row[RESULT_IDX])

    def test_pentad(self):
        """Проверка выбора турниром из пяти участников."""
        test_data = (
            (self.test_func[MAX_VALUE], (1, 2, 3, 4, 5), 5),
            (self.test_func[MIN_VALUE], (1., 2., 3., 4., 5.), 1.),
            (self.test_func[MAX_VALUE], ('a', 'b', 'c', 'd', 'e'), 'e'),
            (self.test_func[MIN_VALUE], ('a', 'b', 'c', 'd', 'e'), 'a'),
            (self.test_func[MAX_LEN], ('aa', 'b', 'ccc', 'aaaa', 'abcde'),
             'abcde'),
            (self.test_func[MIN_LEN], ('aa', 'b', 'ccc', 'aaaa', 'abcde'), 'b'),
        )
        for row in test_data:
            self.assertEqual(tournament(row[SAMPLE_IDX], row[FUNC_IDX]),
                             row[RESULT_IDX])

    def test_random_unique_sample(self):
        """Проверка выбора турниром из случайного набора без повторений."""
        for sample_len in range(2, 1000):
            unique_sample = [i for i in range(sample_len)]
            random.shuffle(unique_sample)
            self.assertEqual(
                tournament(unique_sample, self.test_func[MAX_VALUE]),
                max(unique_sample))
            self.assertEqual(
                tournament(unique_sample, self.test_func[MIN_VALUE]),
                min(unique_sample))

    def test_random_sample_order_asc(self):
        """Проверка выбора турниром из набора упорядоченного по
        возрастанию."""
        for sample_len in range(2, 1000):
            asc_sample = [i for i in range(sample_len)]
            self.assertEqual(
                tournament(asc_sample, self.test_func[MAX_VALUE]),
                max(asc_sample))
            self.assertEqual(
                tournament(asc_sample, self.test_func[MIN_VALUE]),
                min(asc_sample))

    def test_random_sample_order_desc(self):
        """Проверка выбора турниром из набора упорядоченного по
        убыванию."""
        for sample_len in range(2, 1000):
            desc_sample = [i for i in range(sample_len, 0, -1)]
            self.assertEqual(
                tournament(desc_sample, self.test_func[MAX_VALUE]),
                max(desc_sample))
            self.assertEqual(
                tournament(desc_sample, self.test_func[MIN_VALUE]),
                min(desc_sample))

    def test_random_sample(self):
        """Проверка выбора турниром из случайного набора с повторениями."""
        for sample_len in range(2, 1000):
            sample = [i for i in range(sample_len)]
            random.shuffle(sample)
            for step in range(random.randint(0, sample_len)):
                sample.append(random.choice(sample))
            self.assertEqual(tournament(sample, self.test_func[MAX_VALUE]),
                             max(sample))
            self.assertEqual(tournament(sample, self.test_func[MIN_VALUE]),
                             min(sample))


if __name__ == '__main__':
    unittest.main()
