import unittest


from schedule_pack import ScheduleItem
from schedule_pack.abs_schedule import AbstractSchedule
from schedule_pack.conveyor_schedule import ConveyorSchedule
from schedule_pack.errors import ScheduleArgumentError
from schedule_pack.constants import ERR_TASKS_NOT_LIST_MSG, \
    ERR_TASKS_EMPTY_LIST_MSG, ERR_INVALID_TASK_TEMPL, \
    ERR_EXECUTOR_NOT_INT_MSG, ERR_EXECUTOR_OUT_OF_RANGE_MSG, SCHEDULE_STR_TEMPL
from schedule_pack.staged_task import StagedTask


class TestConveyorSchedule(unittest.TestCase):
    def test_class_inheritance(self):
        """Проверяет наследование от класса AbstractSchedule"""
        schedule = ConveyorSchedule([StagedTask('a', [1, 1])])
        self.assertIsInstance(schedule, AbstractSchedule)

    def test_none_tasks(self):
        """Проверяет выброс исключения при передаче некорректного параметра
        списка задач."""
        with self.assertRaises(ScheduleArgumentError) as error:
            ConveyorSchedule(None)
        self.assertEqual(ERR_TASKS_NOT_LIST_MSG, str(error.exception))

    def test_empty_tasks(self):
        """Проверяет выброс исключения при передаче пустого списка задач."""
        with self.assertRaises(ScheduleArgumentError) as error:
            ConveyorSchedule([])
        self.assertEqual(ERR_TASKS_EMPTY_LIST_MSG, str(error.exception))

    def test_tasks_contains_non_task(self):
        """Проверяет выброс исключения при передаче в списке задачи в
        некорректном формате."""
        tasks = [
            StagedTask('a', [1, 1]),
            StagedTask('b', [1, 1]),
            'non task object']
        with self.assertRaises(ScheduleArgumentError) as error:
            ConveyorSchedule(tasks)
        self.assertEqual(ERR_INVALID_TASK_TEMPL.format(2), str(error.exception))

    def test_not_int_executor_idx(self):
        """Проверяет выброс исключения при передаче не корректного индекса
        исполнителя."""
        tasks = [
            StagedTask('a', [1, 1]),
            StagedTask('b', [1, 1])]
        schedule = ConveyorSchedule(tasks)
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
            StagedTask('a', [1, 1]),
            StagedTask('b', [1, 1])]
        schedule = ConveyorSchedule(tasks)
        incorrect_idx = [len(tasks), len(tasks) + 1]
        for idx in incorrect_idx:
            with self.subTest(idx=idx):
                with self.assertRaises(ScheduleArgumentError) as error:
                    schedule.get_schedule_for_executor(idx)
                self.assertEqual(ERR_EXECUTOR_OUT_OF_RANGE_MSG,
                                 str(error.exception))

    def test_str(self):
        """Проверяет корректность приведения расписания к строковому типу."""
        tasks = [
            StagedTask('a', [1, 1]),
            StagedTask('b', [1, 1])]
        schedule = ConveyorSchedule(tasks)
        str_schedule = SCHEDULE_STR_TEMPL.format(3, 2, 2)
        self.assertEqual(str_schedule, str(schedule))

    def test_single_task(self):
        """Проверяет корректность составления расписания для одной задачи."""
        task_a = StagedTask('a', [1, 2])
        schedule = ConveyorSchedule([task_a])
        stage1_schedule = (ScheduleItem(task_a, 0, 1),
                           ScheduleItem(None, 1, 2,
                                        is_downtime=True))
        stage2_schedule = (ScheduleItem(None, 0, 1,
                                        is_downtime=True),
                           ScheduleItem(task_a, 1, 2))
        self.assertEqual(tuple([task_a]), schedule.tasks)
        self.assertEqual(1, schedule.task_count)
        self.assertEqual(3, schedule.duration)
        self.assertEqual(stage1_schedule, schedule.get_schedule_for_executor(0))
        self.assertEqual(stage2_schedule, schedule.get_schedule_for_executor(1))

    def test_double_task(self):
        """Проверяет корректность составления расписания для двух задач."""
        task_a = StagedTask('a', [2, 1])
        task_b = StagedTask('b', [1, 2])
        schedule = ConveyorSchedule([task_a, task_b])
        stage1_schedule = (ScheduleItem(task_b, 0, 1),
                           ScheduleItem(task_a, 1, 2),
                           ScheduleItem(None, 3, 1,
                                        is_downtime=True))
        stage2_schedule = (ScheduleItem(None, 0, 1,
                                        is_downtime=True),
                           ScheduleItem(task_b, 1, 2),
                           ScheduleItem(task_a, 3, 1))
        self.assertEqual(tuple([task_a, task_b]), schedule.tasks)
        self.assertEqual(2, schedule.task_count)
        self.assertEqual(4, schedule.duration)
        self.assertEqual(stage1_schedule, schedule.get_schedule_for_executor(0))
        self.assertEqual(stage2_schedule, schedule.get_schedule_for_executor(1))

    def test_triple_stage2_greater_only(self):
        """Проверяет корректность составления расписания для трех задач,
        где второй этап продолжительнее первого."""
        task_a = StagedTask('a', [1, 2])
        task_b = StagedTask('b', [3, 4])
        task_c = StagedTask('c', [5, 6])
        schedule = ConveyorSchedule([task_a, task_b, task_c])
        stage1_schedule = (ScheduleItem(task_a, 0, 1),
                           ScheduleItem(task_b, 1, 3),
                           ScheduleItem(task_c, 4, 5),
                           ScheduleItem(None, 9, 6,
                                        is_downtime=True))
        stage2_schedule = (ScheduleItem(None, 0, 1,
                                        is_downtime=True),
                           ScheduleItem(task_a, 1, 2),
                           ScheduleItem(None, 3, 1,
                                        is_downtime=True),
                           ScheduleItem(task_b, 4, 4),
                           ScheduleItem(None, 8, 1,
                                        is_downtime=True),
                           ScheduleItem(task_c, 9, 6))
        self.assertEqual(tuple([task_a, task_b, task_c]), schedule.tasks)
        self.assertEqual(3, schedule.task_count)
        self.assertEqual(15, schedule.duration)
        self.assertEqual(stage1_schedule, schedule.get_schedule_for_executor(0))
        self.assertEqual(stage2_schedule, schedule.get_schedule_for_executor(1))

    def test_triple_stage2_less_only(self):
        """Проверяет корректность составления расписания для трех задач,
        где первый этап продолжительнее второго."""
        task_a = StagedTask('a', [2, 1])
        task_b = StagedTask('b', [4, 3])
        task_c = StagedTask('c', [6, 5])
        schedule = ConveyorSchedule([task_a, task_b, task_c])
        stage1_schedule = (ScheduleItem(task_c, 0, 6),
                           ScheduleItem(task_b, 6, 4),
                           ScheduleItem(task_a, 10, 2),
                           ScheduleItem(None, 12, 3,
                                        is_downtime=True))
        stage2_schedule = (ScheduleItem(None, 0, 6,
                                        is_downtime=True),
                           ScheduleItem(task_c, 6, 5),
                           ScheduleItem(task_b, 11, 3),
                           ScheduleItem(task_a, 14, 1))
        self.assertEqual(tuple([task_a, task_b, task_c]), schedule.tasks)
        self.assertEqual(3, schedule.task_count)
        self.assertEqual(15, schedule.duration)
        self.assertEqual(stage1_schedule, schedule.get_schedule_for_executor(0))
        self.assertEqual(stage2_schedule, schedule.get_schedule_for_executor(1))


    def test_triple_mix(self):
        """Проверяет корректность составления расписания для трех задач."""
        task_a = StagedTask('a', [2, 1])
        task_b = StagedTask('b', [3, 4])
        task_c = StagedTask('c', [6, 5])
        schedule = ConveyorSchedule([task_a, task_b, task_c])
        stage1_schedule = (ScheduleItem(task_b, 0, 3),
                           ScheduleItem(task_c, 3, 6),
                           ScheduleItem(task_a, 9, 2),
                           ScheduleItem(None, 11, 4,
                                        is_downtime=True))
        stage2_schedule = (ScheduleItem(None, 0, 3,
                                        is_downtime=True),
                           ScheduleItem(task_b, 3, 4),
                           ScheduleItem(None, 7, 2,
                                        is_downtime=True),
                           ScheduleItem(task_c, 9, 5),
                           ScheduleItem(task_a, 14, 1))
        self.assertEqual(tuple([task_a, task_b, task_c]), schedule.tasks)
        self.assertEqual(3, schedule.task_count)
        self.assertEqual(15, schedule.duration)
        self.assertEqual(stage1_schedule, schedule.get_schedule_for_executor(0))
        self.assertEqual(stage2_schedule, schedule.get_schedule_for_executor(1))

    def test_pentad(self):
        """Проверяет корректность составления расписания для пяти задач."""
        task_a = StagedTask('a', [4, 3])
        task_b = StagedTask('b', [5, 2])
        task_c = StagedTask('c', [3, 5])
        task_d = StagedTask('d', [2, 3])
        task_e = StagedTask('e', [4, 4])
        schedule = ConveyorSchedule([task_a, task_b, task_c, task_d, task_e])
        ordered_tasks = tuple([task_a, task_b, task_c, task_d, task_e])
        stage1_schedule = (ScheduleItem(task_d, 0, 2),
                           ScheduleItem(task_c, 2, 3),
                           ScheduleItem(task_e, 5, 4),
                           ScheduleItem(task_a, 9, 4),
                           ScheduleItem(task_b, 13, 5),
                           ScheduleItem(None, 18, 2,
                                        is_downtime=True))
        stage2_schedule = (ScheduleItem(None, 0, 2,
                                        is_downtime=True),
                           ScheduleItem(task_d, 2, 3),
                           ScheduleItem(task_c, 5, 5),
                           ScheduleItem(task_e, 10, 4),
                           ScheduleItem(task_a, 14, 3),
                           ScheduleItem(None, 17, 1,
                                        is_downtime=True),
                           ScheduleItem(task_b, 18, 2))
        self.assertEqual(ordered_tasks, schedule.tasks)
        self.assertEqual(5, schedule.task_count)
        self.assertEqual(20, schedule.duration)
        self.assertEqual(stage1_schedule, schedule.get_schedule_for_executor(0))
        self.assertEqual(stage2_schedule, schedule.get_schedule_for_executor(1))

    def test_sevenfold(self):
        """Проверяет корректность составления расписания для семи задач."""
        task_a = StagedTask('a', [7, 2])
        task_b = StagedTask('b', [3, 4])
        task_c = StagedTask('c', [2, 5])
        task_d = StagedTask('d', [4, 1])
        task_e = StagedTask('e', [6, 6])
        task_f = StagedTask('f', [5, 3])
        task_g = StagedTask('g', [4, 5])
        schedule = ConveyorSchedule([task_a, task_b, task_c, task_d, task_e,
                                     task_f, task_g])
        tasks = tuple([task_a, task_b, task_c, task_d, task_e, task_f, task_g])
        stage1_schedule = (ScheduleItem(task_c, 0, 2),
                           ScheduleItem(task_b, 2, 3),
                           ScheduleItem(task_g, 5, 4),
                           ScheduleItem(task_e, 9, 6),
                           ScheduleItem(task_f, 15, 5),
                           ScheduleItem(task_a, 20, 7),
                           ScheduleItem(task_d, 27, 4),
                           ScheduleItem(None, 31, 1,
                                        is_downtime=True))
        stage2_schedule = (ScheduleItem(None, 0, 2,
                                        is_downtime=True),
                           ScheduleItem(task_c, 2, 5),
                           ScheduleItem(task_b, 7, 4),
                           ScheduleItem(task_g, 11, 5),
                           ScheduleItem(task_e, 16, 6),
                           ScheduleItem(task_f, 22, 3),
                           ScheduleItem(None, 25, 2,
                                        is_downtime=True),
                           ScheduleItem(task_a, 27, 2),
                           ScheduleItem(None, 29, 2,
                                        is_downtime=True),
                           ScheduleItem(task_d, 31, 1))
        self.assertEqual(tasks, schedule.tasks)
        self.assertEqual(7, schedule.task_count)
        self.assertEqual(32, schedule.duration)
        self.assertEqual(stage1_schedule, schedule.get_schedule_for_executor(0))
        self.assertEqual(stage2_schedule, schedule.get_schedule_for_executor(1))


if __name__ == '__main__':
    unittest.main()
