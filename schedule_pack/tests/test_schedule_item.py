import unittest

from schedule_pack import Task, ScheduleItem
from schedule_pack.errors import ScheduleItemError
from schedule_pack.constants import (ERR_NOT_NONE_TASK_MSG, ERR_NONE_TASK_MSG,
                                     ERR_START_NOT_NUMBER_MSG,
                                     ERR_START_NEG_NUMBER_MSG,
                                     ERR_DUR_NOT_NUMBER_MSG,
                                     ERR_DUR_NOT_POS_NUMBER_MSG,
                                     SCHEDULE_ITEM_DOWNTIME_STR_TEMPL,
                                     SCHEDULE_ITEM_STR_TEMPL)


class TestScheduleItem(unittest.TestCase):
    def test_init_none_task(self):
        """Проверяет выброс исключения при передаче None в качестве задачи"""
        with self.assertRaises(ScheduleItemError) as error:
            ScheduleItem(None, 0, 1, False)
        self.assertEqual(ERR_NONE_TASK_MSG, str(error.exception))

    def test_init_has_task_with_downtime(self):
        """Проверяет выброс исключения при одновременном указании задачи и
        признака простоя"""
        with self.assertRaises(ScheduleItemError) as error:
            ScheduleItem(Task('a', 1), 0, 1, True)
        self.assertEqual(ERR_NOT_NONE_TASK_MSG, str(error.exception))

    def test_init_not_number_start(self):
        """Проверяет выброс исключения при некорректном указании времени
        начала выполнения задачи - передано не число"""
        incorrect_values = [None, 'str', []]
        for value in incorrect_values:
            with self.assertRaises(ScheduleItemError) as error:
                ScheduleItem(None, value, 1, True)
            self.assertEqual(ERR_START_NOT_NUMBER_MSG, str(error.exception))

    def test_init_negative_start(self):
        """Проверяет выброс исключения при указании времени
        начала выполнения задачи меньше нуля"""
        with self.assertRaises(ScheduleItemError) as error:
            ScheduleItem(None, -1, 1, True)
        self.assertEqual(ERR_START_NEG_NUMBER_MSG, str(error.exception))

    def test_init_not_number_duration(self):
        """Проверяет выброс исключения при некорректном указании
        продолжительности выполнения задачи - передано не число"""
        incorrect_values = [None, 'str', []]
        for value in incorrect_values:
            with self.assertRaises(ScheduleItemError) as error:
                ScheduleItem(None, 1, value, True)
            self.assertEqual(ERR_DUR_NOT_NUMBER_MSG, str(error.exception))

    def test_init_not_pos_duration(self):
        """Проверяет выброс исключения при указании продолжительности
        выполнения задачи меньше или равной нулю"""
        incorrect_values = [0, -1, -0.1]
        for value in incorrect_values:
            with self.assertRaises(ScheduleItemError) as error:
                ScheduleItem(None, 1, value, True)
            self.assertEqual(ERR_DUR_NOT_POS_NUMBER_MSG, str(error.exception))

    def test_init_integers(self):
        """Проверяет инициализацию объекта класса с целочисленными значениями"""
        task_name = 'task'
        start = 0
        duration = 1
        row = ScheduleItem(Task(task_name, 1), start, duration)
        self.assertEqual(task_name, row.task_name)
        self.assertEqual(start, row.start)
        self.assertEqual(duration, row.duration)
        self.assertEqual(start + duration, row.end)
        self.assertFalse(row.is_downtime)

    def test_init_floats_downtime(self):
        """Проверяет инициализацию объекта класса с вещественными значениями
        и признаком простоя"""
        start = 1.1
        duration = 0.25
        item = ScheduleItem(None, start, duration, is_downtime=True)
        self.assertEqual('downtime', item.task_name)
        self.assertEqual(start, item.start)
        self.assertEqual(duration, item.duration)
        self.assertEqual(start + duration, item.end)
        self.assertTrue(item.is_downtime)
        err = SCHEDULE_ITEM_DOWNTIME_STR_TEMPL.format(start, start + duration)
        self.assertEqual(err, str(item))

    def test_str(self):
        """Проверка приведения объекта класса без простоя к строковому типу"""
        task_name = 'task'
        start = 0
        duration = 1
        item = ScheduleItem(Task(task_name, duration), start, duration)
        str_item = SCHEDULE_ITEM_STR_TEMPL.format(task_name, start,
                                                  start + duration)
        self.assertEqual(str_item, str(item))

    def test_str_downtime(self):
        """Проверка приведения объекта класса с простоем к строковому типу"""
        start = 1.1
        duration = 10
        item = ScheduleItem(None, start, duration, is_downtime=True)
        str_item = SCHEDULE_ITEM_DOWNTIME_STR_TEMPL.format(start,
                                                           start + duration)
        self.assertEqual(str_item, str(item))


if __name__ == '__main__':
    unittest.main()
