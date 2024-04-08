from schedule_pack.abs_schedule import AbstractSchedule
from schedule_pack.task import Task
from schedule_pack.schedule_item import ScheduleItem
from schedule_pack.constants import SCHEDULE_STR_TEMPL


class Schedule(AbstractSchedule):
    """Класс представляет оптимальное расписание для списка задач и количества
    исполнителей. Для построения расписания используется Ленточная стратегия.

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

    def __init__(self, tasks: list[Task], executor_count: int):
        """Конструктор для инициализации объекта расписания.

        :param tasks: Список задач для составления расписания.
        :param executor_count: Количество исполнителей.
        :raise ScheduleArgumentError: Если список задач предоставлен в
        некорректном формате или количество исполнителей не является целым
        положительным числом.
        """
        super().__init__(tasks, executor_count)

        # Рассчитывается и сохраняется в приватном поле класса минимальная
        # продолжительность расписания
        self._duration = self.__calculate_duration()

        # Процедура заполняет пустую заготовку расписания для каждого
        # исполнителя объектами ScheduleItem.
        self.__fill_schedule_for_each_executor()

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._duration

    def __calculate_duration(self) -> float:
        """Вычисляет и возвращает минимальную продолжительность расписания"""
        avg_duration = (sum([task.duration for task in self._tasks])
                        / self.executor_count)
        max_duration = max([task.duration for task in self._tasks])
        return max(float(max_duration), avg_duration)

    def __fill_schedule_for_each_executor(self) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, на основе исходного списка задач и общей продолжительности
        расписания."""
        task_idx = 0
        part_after_gap = 0
        for executor_idx in range(self.executor_count):
            executor_duration = self._duration
            while executor_duration > 0 and task_idx < self.task_count:
                current_task = self._tasks[task_idx]
                if part_after_gap > 0:
                    part = part_after_gap
                    part_after_gap = 0
                    task_idx += 1
                elif current_task.duration <= executor_duration:
                    part = current_task.duration
                    task_idx += 1
                else:
                    part = executor_duration
                    part_after_gap = current_task.duration - executor_duration
                start = self._duration - executor_duration
                executor_duration -= part
                self._executor_schedule[executor_idx].append(
                    ScheduleItem(current_task, start, part))
            if executor_duration > 0:
                start = self._duration - executor_duration
                self._executor_schedule[executor_idx].append(
                    ScheduleItem(None, start, executor_duration,
                                 is_downtime=True))


if __name__ == '__main__':
    print('Пример использования класса Schedule')

    # Инициализируем входные данные для составления расписания
    tasks = [Task('a', 3), Task('b', 4), Task('c', 6), Task('d', 7),
             Task('e', 7), Task('f', 9), Task('g', 10), Task('h', 12),
             Task('i', 17)]

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = Schedule(tasks, 5)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f'\nРасписание для исполнителя # {i + 1}:')
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)
