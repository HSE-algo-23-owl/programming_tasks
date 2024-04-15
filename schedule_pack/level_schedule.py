import networkx as nx

from schedule_pack import Task
from schedule_pack.abs_schedule import AbstractSchedule
from schedule_pack.errors import ScheduleArgumentError
from graph_pack.graph_validator import GraphValidator
from schedule_pack.schedule_item import ScheduleItem


class LevelSchedule(AbstractSchedule):
    """Класс представляет оптимальное расписание для списка задач. Все задачи
    единичной длительности и могут зависеть друг от друга. Для построения
    расписания используется уровневая стратегия.

    Properties
    ----------
    tasks(self) -> tuple[Task]:
        Возвращает исходный список задач для составления расписания.

    task_count(self) -> int:
        Возвращает количество задач для составления расписания.

    executor_count(self) -> int:
        Возвращает количество исполнителей.

    duration(self) -> float:
        Возвращает общую продолжительность расписания.

    Methods
    -------
    get_schedule_for_executor(self, executor_idx: int) -> tuple[ScheduleRow]:
        Возвращает расписание для указанного исполнителя.
    """

    def __init__(self, graph: nx.Graph, executor_count: int):
        """Конструктор для инициализации объекта расписания.

        :param graph: Граф, представляющий зависимость между задачами.
        :param executor_count: Количество исполнителей.
        :raise ScheduleArgumentError: Если количество исполнителей не является
        целым положительным числом.
        """
        if GraphValidator.graph_has_loop(graph):
            raise ScheduleArgumentError('Граф содержит цикл')
        if not GraphValidator.is_inverted_trees(graph):
            raise ScheduleArgumentError('Граф не является обратно '
                                        'ориентированным деревом или лесом из '
                                        'обратно ориентированных деревьев')

        self.__graph = graph
        self.__matrix = (nx.adjacency_matrix(graph)).toarray()
        super().__init__(self.__get_tasks_from_graph(), executor_count)
        self.__fill_schedule()

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._executor_schedule[0][-1].end

    def __get_tasks_from_graph(self):
        """Возвращает список задач на основе вершин графа."""
        return [Task(node_name, 1)
                for node_name in list(self.__graph.nodes.keys())]

    def __fill_schedule(self) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, согласно уровневой стратегии."""
        pass


if __name__ == '__main__':
    print('Пример использования класса LevelSchedule')

    # Инициализируем входные данные для составления расписания
    graph = nx.DiGraph()
    graph.add_nodes_from(['a', 'b', 'c', 'd', 'e'])
    graph.add_edges_from([('c', 'b'), ('b', 'a'), ('e', 'a'), ('d', 'e')])

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = LevelSchedule(graph, 2)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f'\nРасписание для исполнителя # {i + 1}:')
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)
