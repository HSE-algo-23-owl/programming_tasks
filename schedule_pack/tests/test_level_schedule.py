import unittest
import networkx as nx

from schedule_pack import ScheduleItem, Task
from schedule_pack.abs_schedule import AbstractSchedule
from schedule_pack.errors import ScheduleArgumentError
from schedule_pack.constants import ERR_EXECUTOR_NOT_INT_MSG, \
    ERR_EXECUTOR_OUT_OF_RANGE_MSG, SCHEDULE_STR_TEMPL
from schedule_pack.level_schedule import LevelSchedule


class TestLevelSchedule(unittest.TestCase):
    graph = nx.DiGraph()

    def setUp(self):
        self.graph = nx.DiGraph()

    def __check_schedule(self, schedule: LevelSchedule, graph: nx.Graph):
        """Проверяет корректность составленного расписания"""
        task_names = list(graph.nodes.keys())
        task_start_dict = {}
        for idx in range(schedule.executor_count):
            ex_schedule = schedule.get_schedule_for_executor(idx)
            # расписания для всех исполнителей должны быть одинаковой длины
            if ex_schedule[-1].end != schedule.duration:
                return False
            prev_end = 0
            for row in ex_schedule:
                # Текущее задание должно начинаться в момент окончания
                # предыдущего
                if row.start != prev_end:
                    return False
                prev_end = row.end
                if row.is_downtime:
                    continue
                # Задание должно быть включено в список
                if row.task_name not in task_names:
                    return False
                # Задание должно встречаться в расписании только один раз
                if row.task_name in task_start_dict:
                    return False
                task_start_dict[row.task_name] = row.start
        for (src, trg) in graph.edges:
            # Дочернее задание должно начинаться после окончания родительского
            if task_start_dict[src] >= task_start_dict[trg]:
                return False
        return True

    def test_class_inheritance(self):
        """Проверяет наследование от класса AbstractSchedule"""
        self.graph.add_nodes_from(['a'])
        schedule = LevelSchedule(self.graph, 1)
        self.assertIsInstance(schedule, AbstractSchedule)

    def test_not_int_executor_idx(self):
        """Проверяет выброс исключения при передаче не корректного индекса
        исполнителя."""
        self.graph.add_nodes_from(['a'])
        schedule = LevelSchedule(self.graph, 1)
        incorrect_idx = [-1, 1.1, None, 'str', []]
        for idx in incorrect_idx:
            with self.subTest(idx=idx):
                with self.assertRaises(ScheduleArgumentError) as error:
                    schedule.get_schedule_for_executor(idx)
                self.assertEqual(ERR_EXECUTOR_NOT_INT_MSG, str(error.exception))

    def test_out_of_range_executor_idx(self):
        """Проверяет выброс исключения при передаче не корректного индекса
        исполнителя."""
        self.graph.add_nodes_from(['a'])
        schedule = LevelSchedule(self.graph, 1)
        incorrect_idx = [1, 2]
        for idx in incorrect_idx:
            with self.subTest(idx=idx):
                with self.assertRaises(ScheduleArgumentError) as error:
                    schedule.get_schedule_for_executor(idx)
                self.assertEqual(ERR_EXECUTOR_OUT_OF_RANGE_MSG,
                                 str(error.exception))

    def test_str(self):
        """Проверяет корректность приведения расписания к строковому типу."""
        self.graph.add_nodes_from(['a'])
        schedule = LevelSchedule(self.graph, 1)
        str_schedule = SCHEDULE_STR_TEMPL.format(1, 1, 1)
        self.assertEqual(str_schedule, str(schedule))

    def test_1tree_1task_1exec(self):
        """Проверяет расписание для 1 дерева, 1 задачи и 1 исполнителя."""
        self.graph.add_nodes_from(['a'])
        schedule = LevelSchedule(self.graph, 1)
        task_a = Task('a', 1)
        ex1_schedule = (ScheduleItem(task_a, 0, 1),)
        self.assertEqual(tuple([task_a]), schedule.tasks)
        self.assertEqual(1, schedule.task_count)
        self.assertEqual(1, schedule.duration)
        self.assertEqual(ex1_schedule, schedule.get_schedule_for_executor(0))
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_1tree_2task_1exec(self):
        """Проверяет расписание для 1 дерева, 2 задач и 1 исполнителя."""
        self.graph.add_nodes_from(['a', 'b'])
        self.graph.add_edges_from([('b', 'a')])
        schedule = LevelSchedule(self.graph, 1)
        task_a = Task('a', 1)
        task_b = Task('b', 1)
        ex1_schedule = (ScheduleItem(task_b, 0, 1),
                        ScheduleItem(task_a, 1, 1),)
        self.assertEqual(tuple([task_a, task_b]), schedule.tasks)
        self.assertEqual(2, schedule.task_count)
        self.assertEqual(2, schedule.duration)
        self.assertEqual(ex1_schedule, schedule.get_schedule_for_executor(0))
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_1tree_3task_1exec(self):
        """Проверяет расписание для 1 дерева, 3 задач и 1 исполнителя."""
        self.graph.add_nodes_from(['a', 'b', 'c'])
        self.graph.add_edges_from([('c', 'a'), ('b', 'a')])
        schedule = LevelSchedule(self.graph, 1)
        task_a = Task('a', 1)
        task_b = Task('b', 1)
        task_c = Task('c', 1)
        self.assertEqual(tuple([task_a, task_b, task_c]), schedule.tasks)
        self.assertEqual(3, schedule.task_count)
        self.assertEqual(3, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_1tree_3task_2exec(self):
        """Проверяет расписание для 1 дерева, 3 задач и 2 исполнителей."""
        self.graph.add_nodes_from(['a', 'b', 'c'])
        self.graph.add_edges_from([('c', 'a'), ('b', 'a')])
        schedule = LevelSchedule(self.graph, 2)
        task_a = Task('a', 1)
        task_b = Task('b', 1)
        task_c = Task('c', 1)
        self.assertEqual(tuple([task_a, task_b, task_c]), schedule.tasks)
        self.assertEqual(3, schedule.task_count)
        self.assertEqual(2, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_1tree_3task_3exec(self):
        """Проверяет расписание для 1 дерева, 3 задач и 3 исполнителей."""
        self.graph.add_nodes_from(['a', 'b', 'c'])
        self.graph.add_edges_from([('c', 'a'), ('b', 'a')])
        schedule = LevelSchedule(self.graph, 2)
        task_a = Task('a', 1)
        task_b = Task('b', 1)
        task_c = Task('c', 1)
        self.assertEqual(tuple([task_a, task_b, task_c]), schedule.tasks)
        self.assertEqual(3, schedule.task_count)
        self.assertEqual(2, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_1tree_5task_2exec(self):
        """Проверяет расписание для 1 дерева, 5 задач и 2 исполнителей."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e'])
        self.graph.add_edges_from([('c', 'b'), ('b', 'a'), ('e', 'a'), ('d', 'e')])
        schedule = LevelSchedule(self.graph, 2)
        task_a = Task('a', 1)
        task_b = Task('b', 1)
        task_c = Task('c', 1)
        task_d = Task('d', 1)
        task_e = Task('e', 1)
        self.assertEqual(tuple([task_a, task_b, task_c, task_d, task_e]),
                         schedule.tasks)
        self.assertEqual(5, schedule.task_count)
        self.assertEqual(3, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_2tree_2task_1exec(self):
        """Проверяет расписание для 2 деревьев, 2 задач и 1 исполнителя."""
        self.graph.add_nodes_from(['a', 'b'])
        schedule = LevelSchedule(self.graph, 1)
        task_a = Task('a', 1)
        task_b = Task('b', 1)
        self.assertEqual(tuple([task_a, task_b]), schedule.tasks)
        self.assertEqual(2, schedule.task_count)
        self.assertEqual(2, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_2tree_5task_2exec(self):
        """Проверяет расписание для 2 деревьев, 5 задач и 2 исполнителей."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e'])
        self.graph.add_edges_from([('c', 'a'), ('b', 'a'), ('e', 'd')])
        schedule = LevelSchedule(self.graph, 2)
        task_a = Task('a', 1)
        task_b = Task('b', 1)
        task_c = Task('c', 1)
        task_d = Task('d', 1)
        task_e = Task('e', 1)
        self.assertEqual(tuple([task_a, task_b, task_c, task_d, task_e]),
                         schedule.tasks)
        self.assertEqual(5, schedule.task_count)
        self.assertEqual(3, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_2tree_5task_3exec(self):
        """Проверяет расписание для 2 деревьев, 5 задач и 3 исполнителей."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e'])
        self.graph.add_edges_from([('c', 'a'), ('b', 'a'), ('e', 'd')])
        schedule = LevelSchedule(self.graph, 3)
        task_a = Task('a', 1)
        task_b = Task('b', 1)
        task_c = Task('c', 1)
        task_d = Task('d', 1)
        task_e = Task('e', 1)
        self.assertEqual(tuple([task_a, task_b, task_c, task_d, task_e]),
                         schedule.tasks)
        self.assertEqual(5, schedule.task_count)
        self.assertEqual(2, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_2tree_6task_4exec(self):
        """Проверяет расписание для 2 деревьев, 6 задач и 4 исполнителей."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f'])
        self.graph.add_edges_from([('c', 'a'), ('b', 'a'), ('e', 'd'),
                                   ('f', 'e')])
        schedule = LevelSchedule(self.graph, 4)
        task_a = Task('a', 1)
        task_b = Task('b', 1)
        task_c = Task('c', 1)
        task_d = Task('d', 1)
        task_e = Task('e', 1)
        task_f = Task('f', 1)
        self.assertEqual(tuple([task_a, task_b, task_c, task_d, task_e,
                                task_f]), schedule.tasks)
        self.assertEqual(6, schedule.task_count)
        self.assertEqual(3, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_3tree_13task_2exec(self):
        """Проверяет расписание для 3 деревьев, 13 задач и 2 исполнителей."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                                   'j', 'k', 'l', 'm'])
        self.graph.add_edges_from([('d', 'a'), ('j', 'd'), ('e', 'b'),
                                   ('f', 'b'), ('k', 'e'), ('g', 'c'),
                                   ('h', 'c'), ('i', 'c'), ('l', 'g'),
                                   ('m', 'g')])
        schedule = LevelSchedule(self.graph, 2)
        self.assertEqual(13, schedule.task_count)
        self.assertEqual(7, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_3tree_13task_3exec(self):
        """Проверяет расписание для 3 деревьев, 13 задач и 3 исполнителей."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                                   'j', 'k', 'l', 'm'])
        self.graph.add_edges_from([('d', 'a'), ('j', 'd'), ('e', 'b'),
                                   ('f', 'b'), ('k', 'e'), ('g', 'c'),
                                   ('h', 'c'), ('i', 'c'), ('l', 'g'),
                                   ('m', 'g')])
        schedule = LevelSchedule(self.graph, 3)
        self.assertEqual(13, schedule.task_count)
        self.assertEqual(5, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_3tree_13task_4exec(self):
        """Проверяет расписание для 3 деревьев, 13 задач и 4 исполнителей."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                                   'j', 'k', 'l', 'm'])
        self.graph.add_edges_from([('d', 'a'), ('j', 'd'), ('e', 'b'),
                                   ('f', 'b'), ('k', 'e'), ('g', 'c'),
                                   ('h', 'c'), ('i', 'c'), ('l', 'g'),
                                   ('m', 'g')])
        schedule = LevelSchedule(self.graph, 4)
        self.assertEqual(13, schedule.task_count)
        self.assertEqual(4, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))

    def test_1tree_12task_2exec(self):
        """Проверяет расписание для 1 дерева, 13 задач и 2 исполнителей."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                                   'j', 'k', 'l', 'm'])
        self.graph.add_edges_from([('b', 'e'), ('c', 'b'), ('d', 'a'),
                                   ('e', 'a'), ('f', 'b'), ('g', 'l'),
                                   ('h', 'l'), ('i', 'c'), ('j', 'c'),
                                   ('k', 'd'), ('l', 'd'), ('m', 'l')])
        schedule = LevelSchedule(self.graph, 2)
        self.assertEqual(13, schedule.task_count)
        self.assertEqual(7, schedule.duration)
        self.assertTrue(self.__check_schedule(schedule, self.graph))


if __name__ == '__main__':
    unittest.main()
