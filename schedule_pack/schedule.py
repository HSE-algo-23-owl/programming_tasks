from schedule_pack.task import Task
from schedule_pack.schedule_item import ScheduleItem
from schedule_pack.errors import ScheduleArgumentError
from schedule_pack.constants import ERR_TASKS_NOT_LIST_MSG,\
    ERR_TASKS_EMPTY_LIST_MSG, ERR_INVALID_TASK_TEMPL, \
    ERR_EXECUTOR_NOT_INT_MSG, ERR_EXECUTOR_OUT_OF_RANGE_MSG, SCHEDULE_STR_TEMPL


class Schedule:
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
        Schedule.__validate_params(tasks)

        # Сохраняем исходный список задач в приватном поле класса
        self.__tasks = tasks

        # Для каждого исполнителя создается пустая заготовка для расписания
        self.__executor_schedule: list[list[ScheduleItem]] = \
            [[] for _ in range(executor_count)]

        # Рассчитывается и сохраняется в приватном поле класса минимальная
        # продолжительность расписания
        self.__duration = self.__calculate_duration()

        # Процедура заполняет пустую заготовку расписания для каждого
        # исполнителя объектами ScheduleItem.
        self.__fill_schedule_for_each_executor()

    def __str__(self):
        return SCHEDULE_STR_TEMPL.format(self.duration, self.task_count,
                                         self.executor_count)

    @property
    def tasks(self) -> tuple[Task]:
        """Возвращает исходный список задач для составления расписания."""
        return tuple(self.__tasks)

    @property
    def task_count(self) -> int:
        """Возвращает количество задач для составления расписания."""
        return len(self.__tasks)

    @property
    def executor_count(self) -> int:
        """Возвращает количество исполнителей."""
        return len(self.__executor_schedule)

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self.__duration

    def get_schedule_for_executor(self, executor_idx: int) -> \
            tuple[ScheduleItem]:
        """Возвращает расписание для указанного исполнителя.

        :param executor_idx: Индекс исполнителя.
        :raise ScheduleArgumentError: Если индекс исполнителя не является целым
         положительным числом или превышает количество исполнителей.
        :return: Расписание для указанного исполнителя.


        """
        self.__validate_executor_idx(executor_idx)
        return tuple(self.__executor_schedule[executor_idx])

    def __calculate_duration(self) -> float:
        """Вычисляет и возвращает минимальную продолжительность расписания"""
        Tmax = max(task.duration for task in self.__tasks)
        Tavg = sum(task.duration for task in self.__tasks) / self.executor_count
        self.__duration = max(Tmax, Tavg)
        return self.__duration

    def __fill_schedule_for_each_executor(self) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, на основе исходного списка задач и общей продолжительности
        расписания."""
        task_idx = 0
        remain_duration = 0
        for executor_idx in range(len(self.__executor_schedule)):
            free_time = self.__duration
            while free_time > 0:
                if task_idx >= self.task_count:
                    self.__executor_schedule[executor_idx].append(ScheduleItem(None, self.__duration - free_time, free_time, True))
                    free_time = 0
                    continue
                if remain_duration == 0:
                    if (free_time >= self.tasks[task_idx].duration):
                        self.__executor_schedule[executor_idx].append(ScheduleItem(self.__tasks[task_idx], self.__duration - free_time, self.tasks[task_idx].duration))
                        free_time -= self.tasks[task_idx].duration
                        task_idx = task_idx + 1
                    else:
                        self.__executor_schedule[executor_idx].append(
                            ScheduleItem(self.__tasks[task_idx], self.__duration - free_time,
                                         free_time))
                        remain_duration = self.tasks[task_idx].duration - free_time
                        free_time = 0
                else:
                    self.__executor_schedule[executor_idx].append(ScheduleItem(self.__tasks[task_idx], self.__duration - free_time, remain_duration))
                    free_time -= remain_duration
                    task_idx = task_idx + 1
                    remain_duration = 0






    @staticmethod
    def __validate_params(tasks: list[Task]) -> None:
        """Проводит валидацию входящих параметров для инициализации объекта
        класса Schedule."""
        if not isinstance(tasks, list):
            raise ScheduleArgumentError(ERR_TASKS_NOT_LIST_MSG)
        if len(tasks) < 1:
            raise ScheduleArgumentError(ERR_TASKS_EMPTY_LIST_MSG)
        for idx, value in enumerate(tasks):
            if not isinstance(value, Task):
                raise ScheduleArgumentError(ERR_INVALID_TASK_TEMPL.format(idx))

    def __validate_executor_idx(self, executor_idx: int) -> None:
        """Проводит валидацию индекса исполнителя."""
        if not isinstance(executor_idx, int) or executor_idx < 0:
            raise ScheduleArgumentError(ERR_EXECUTOR_NOT_INT_MSG)
        if executor_idx >= self.executor_count:
            raise ScheduleArgumentError(ERR_EXECUTOR_OUT_OF_RANGE_MSG)


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
