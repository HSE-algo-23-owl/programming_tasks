import unittest


from schedule_pack import Schedule, ScheduleItem, Task
from schedule_pack.errors import ScheduleArgumentError
from schedule_pack.constants import ERR_TASKS_NOT_LIST_MSG, \
    ERR_TASKS_EMPTY_LIST_MSG, ERR_INVALID_TASK_TEMPL, \
    ERR_EXECUTOR_NOT_INT_MSG, ERR_EXECUTOR_OUT_OF_RANGE_MSG, SCHEDULE_STR_TEMPL


class TestSchedule(unittest.TestCase):
    def test_none_tasks(self):
        """Проверяет выброс исключения при передаче некорректного параметра
        списка задач."""
        with self.assertRaises(ScheduleArgumentError) as error:
            Schedule(None, 1)
        self.assertEqual(ERR_TASKS_NOT_LIST_MSG, str(error.exception))

    def test_empty_tasks(self):
        """Проверяет выброс исключения при передаче пустого списка задач."""
        with self.assertRaises(ScheduleArgumentError) as error:
            Schedule([], 1)
        self.assertEqual(ERR_TASKS_EMPTY_LIST_MSG, str(error.exception))

    def test_tasks_contains_non_task(self):
        """Проверяет выброс исключения при передаче в списке задачи в
        некорректном формате."""
        tasks = [
            Task('a', 7),
            Task('b', 3),
            'non task object']
        with self.assertRaises(ScheduleArgumentError) as error:
            Schedule(tasks, 1)
        self.assertEqual(ERR_INVALID_TASK_TEMPL.format(2), str(error.exception))

    def test_not_int_executor_idx(self):
        """Проверяет выброс исключения при передаче не корректного индекса
        исполнителя."""
        tasks = [
            Task('a', 7),
            Task('b', 3)]
        schedule = Schedule(tasks, 1)
        incorrect_idx = [-1, 1.1, None, 'str', []]
        for idx in incorrect_idx:
            with self.subTest(idx=idx):
                with self.assertRaises(ScheduleArgumentError) as error:
                    schedule.get_schedule_for_executor(idx)
                self.assertEqual(ERR_EXECUTOR_NOT_INT_MSG, str(error.exception))

    def test_out_of_range_executor_idx(self):
        """Проверяет выброс исключения при передаче не корректного индекса
        исполнителя."""
        tasks = [
            Task('a', 7),
            Task('b', 3)]
        schedule = Schedule(tasks, 1)
        incorrect_idx = [len(tasks), len(tasks) + 1]
        for idx in incorrect_idx:
            with self.subTest(idx=idx):
                with self.assertRaises(ScheduleArgumentError) as error:
                    schedule.get_schedule_for_executor(idx)
                self.assertEqual(ERR_EXECUTOR_OUT_OF_RANGE_MSG,
                                 str(error.exception))

    def test_str(self):
        """Проверяет корректность приведения расписания к строковому типу."""
        task_a = Task('a', 1)
        schedule = Schedule([task_a], 1)
        str_schedule = SCHEDULE_STR_TEMPL.format(1, 1, 1)
        self.assertEqual(str_schedule, str(schedule))

    def test_single_task_single_executor(self):
        """Проверяет корректность составления расписания для одного исполнителя
        и одной задачи."""
        task_a = Task('a', 1)
        schedule = Schedule([task_a], 1)
        executor1_schedule = [ScheduleItem(task_a, 0, task_a.duration)]
        self.assertEqual(tuple([task_a]), schedule.tasks)
        self.assertEqual(1, schedule.task_count)
        self.assertEqual(1, schedule.executor_count)
        self.assertEqual(1, schedule.duration)
        self.assertCountEqual(executor1_schedule,
                              schedule.get_schedule_for_executor(0))

    def test_double_task_single_executor(self):
        """Проверяет корректность составления расписания для одного исполнителя
        и двух задач."""
        task_a = Task('a', 2)
        task_b = Task('b', 1)
        schedule = Schedule([task_a, task_b], 1)
        executor1_schedule = [ScheduleItem(task_a, 0, task_a.duration),
                              ScheduleItem(task_b, task_a.duration,
                                           task_b.duration)]
        self.assertEqual(tuple([task_a, task_b]), schedule.tasks)
        self.assertEqual(2, schedule.task_count)
        self.assertEqual(1, schedule.executor_count)
        self.assertEqual(3, schedule.duration)
        self.assertCountEqual(executor1_schedule,
                              schedule.get_schedule_for_executor(0))

    def test_triple_task_single_executor(self):
        """Проверяет корректность составления расписания для одного исполнителя
        и трех задач."""
        task_a = Task('a', 1)
        task_b = Task('b', 3)
        task_c = Task('c', 5)
        schedule = Schedule([task_a, task_b, task_c], 1)
        executor1_schedule = [ScheduleItem(task_a, 0, task_a.duration),
                              ScheduleItem(task_b, task_a.duration,
                                           task_b.duration),
                              ScheduleItem(task_c,
                                           task_a.duration + task_b.duration,
                                           task_c.duration)]
        self.assertEqual(tuple([task_a, task_b, task_c]), schedule.tasks)
        self.assertEqual(3, schedule.task_count)
        self.assertEqual(1, schedule.executor_count)
        self.assertEqual(9, schedule.duration)
        self.assertCountEqual(executor1_schedule,
                              schedule.get_schedule_for_executor(0))

    def test_single_task_double_executor(self):
        """Проверяет корректность составления расписания для двух исполнителей
        и одной задачи."""
        task_a = Task('a', 1)
        schedule = Schedule([task_a], 2)
        executor1_schedule = [ScheduleItem(task_a, 0, task_a.duration)]
        executor2_schedule = [ScheduleItem(None, 0, task_a.duration,
                                           is_downtime=True)]
        self.assertEqual(2, schedule.executor_count)
        self.assertEqual(1, schedule.duration)
        self.assertCountEqual(executor1_schedule,
                              schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor2_schedule,
                              schedule.get_schedule_for_executor(1))

    def test_double_task_double_executor(self):
        """Проверяет корректность составления расписания для двух исполнителей
        и двух задач."""
        task_a = Task('a', 2)
        task_b = Task('b', 1)
        schedule = Schedule([task_a, task_b], 2)
        executor1_schedule = [ScheduleItem(task_a, 0, task_a.duration)]
        executor2_schedule = [ScheduleItem(task_b, 0, task_b.duration),
                              ScheduleItem(None, 1, 1,
                                           is_downtime=True)]
        self.assertEqual(2, schedule.executor_count)
        self.assertEqual(2, schedule.duration)
        self.assertCountEqual(executor1_schedule,
                              schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor2_schedule,
                              schedule.get_schedule_for_executor(1))

    def test_triple_task_double_executor(self):
        """Проверяет корректность составления расписания для двух исполнителей
        и трех задач."""
        task_a = Task('a', 2)
        task_b = Task('b', 4)
        task_c = Task('c', 6)
        schedule = Schedule([task_a, task_b, task_c], 2)
        executor1_schedule = [ScheduleItem(task_a, 0, task_a.duration),
                              ScheduleItem(task_b, 2, task_b.duration)]
        executor2_schedule = [ScheduleItem(task_c, 0, task_c.duration)]
        self.assertEqual(2, schedule.executor_count)
        self.assertEqual(6, schedule.duration)
        self.assertCountEqual(executor1_schedule,
                              schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor2_schedule,
                              schedule.get_schedule_for_executor(1))

    def test_triple_task_triple_executor(self):
        """Проверяет корректность составления расписания для трех исполнителей
        и трех задач с простоем последнего исполнителя."""
        task_a = Task('a', 2)
        task_b = Task('b', 4)
        task_c = Task('c', 6)
        schedule = Schedule([task_a, task_b, task_c], 3)
        executor1_schedule = [ScheduleItem(task_a, 0, task_a.duration),
                              ScheduleItem(task_b, 2, task_b.duration)]
        executor2_schedule = [ScheduleItem(task_c, 0, task_c.duration)]
        executor3_schedule = [ScheduleItem(None, 0, 6,
                                           is_downtime=True)]
        self.assertEqual(3, schedule.executor_count)
        self.assertEqual(6, schedule.duration)
        self.assertCountEqual(executor1_schedule,
                              schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor2_schedule,
                              schedule.get_schedule_for_executor(1))
        self.assertCountEqual(executor3_schedule,
                              schedule.get_schedule_for_executor(2))

    def test_triple_equal_task_triple_executor(self):
        """Проверяет корректность составления расписания для трех исполнителей
        и трех задач без простоев."""
        task_a = Task('a', 1)
        task_b = Task('b', 1)
        task_c = Task('c', 1)
        schedule = Schedule([task_a, task_b, task_c], 3)
        executor1_schedule = [ScheduleItem(task_a, 0, 1)]
        executor2_schedule = [ScheduleItem(task_b, 0, 1)]
        executor3_schedule = [ScheduleItem(task_c, 0, 1)]
        self.assertEqual(3, schedule.executor_count)
        self.assertEqual(1, schedule.duration)
        self.assertCountEqual(executor1_schedule,
                              schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor2_schedule,
                              schedule.get_schedule_for_executor(1))
        self.assertCountEqual(executor3_schedule,
                              schedule.get_schedule_for_executor(2))

    def test_triple_has_large_task_triple_executor(self):
        """Проверяет корректность составления расписания для трех исполнителей
        и трех задач с простоем для двух исполнителей."""
        task_a = Task('a', 1)
        task_b = Task('b', 1)
        task_c = Task('c', 10)
        schedule = Schedule([task_a, task_b, task_c], 3)
        executor1_schedule = [ScheduleItem(task_a, 0, task_a.duration),
                              ScheduleItem(task_b, 1, task_b.duration),
                              ScheduleItem(task_c, 2, 8)]
        executor2_schedule = [ScheduleItem(task_c, 0, 2),
                              ScheduleItem(None, 2, 8,
                                           is_downtime=True)]
        executor3_schedule = [ScheduleItem(None, 0, 10,
                                           is_downtime=True)]
        self.assertEqual(10, schedule.duration)
        self.assertCountEqual(executor1_schedule,
                              schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor2_schedule,
                              schedule.get_schedule_for_executor(1))
        self.assertCountEqual(executor3_schedule,
                              schedule.get_schedule_for_executor(2))

    def test_complex(self):
        """Проверяет корректность составления расписания для пяти исполнителей
        и девяти задач."""
        task_a = Task('a', 3)
        task_b = Task('b', 4)
        task_c = Task('c', 6)
        task_d = Task('d', 7)
        task_e = Task('e', 7)
        task_f = Task('f', 9)
        task_g = Task('g', 10)
        task_h = Task('h', 12)
        task_i = Task('i', 17)
        tasks = [task_a, task_b, task_c, task_d, task_e, task_f, task_g,
                 task_h, task_i]
        schedule = Schedule(tasks, 5)
        executor1_schedule = [ScheduleItem(task_a, 0, 3),
                              ScheduleItem(task_b, 3, 4),
                              ScheduleItem(task_c, 7, 6),
                              ScheduleItem(task_d, 13, 4)]
        executor2_schedule = [ScheduleItem(task_d, 0, 3),
                              ScheduleItem(task_e, 3, 7),
                              ScheduleItem(task_f, 10, 7)]
        executor3_schedule = [ScheduleItem(task_f, 0, 2),
                              ScheduleItem(task_g, 2, 10),
                              ScheduleItem(task_h, 12, 5)]
        executor4_schedule = [ScheduleItem(task_h, 0, 7),
                              ScheduleItem(task_i, 7, 10)]
        executor5_schedule = [ScheduleItem(task_i, 0, 7),
                              ScheduleItem(None, 7, 10,
                                           is_downtime=True)]
        self.assertEqual(tuple(tasks), schedule.tasks)
        self.assertEqual(9, schedule.task_count)
        self.assertEqual(5, schedule.executor_count)
        self.assertEqual(17, schedule.duration)
        self.assertCountEqual(executor1_schedule,
                              schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor2_schedule,
                              schedule.get_schedule_for_executor(1))
        self.assertCountEqual(executor3_schedule,
                              schedule.get_schedule_for_executor(2))
        self.assertCountEqual(executor4_schedule,
                              schedule.get_schedule_for_executor(3))
        self.assertCountEqual(executor5_schedule,
                              schedule.get_schedule_for_executor(4))


if __name__ == '__main__':
    unittest.main()
