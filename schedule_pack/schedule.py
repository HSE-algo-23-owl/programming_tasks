from schedule_pack.task import Task
from schedule_pack.schedule_item import ScheduleItem
from schedule_pack.errors import ScheduleArgumentError
from schedule_pack.constants import ERR_TASKS_NOT_LIST_MSG, \
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
        sum = 0
        list_dur = []
        for i in self.__tasks:
            list_dur.append(i.duration)
            sum += i.duration
        return max(max(list_dur), sum / self.executor_count)

    def __fill_schedule_for_each_executor(self) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, на основе исходного списка задач и общей продолжительности
        расписания."""
        task = 0
        min_time = self.__duration
        worker = 0
        task_time = 0
        dura = 0
        check = True
        while task_time <= min_time and task < len(self.__tasks):
            if not check:
                current_task_time = dura
                check = True
            else:
                current_task_time = self.tasks[task].duration
            start = task_time
            if task_time + current_task_time <= min_time:
                task_time += current_task_time
                self.__executor_schedule[worker].append(ScheduleItem(self.__tasks[task], start, current_task_time))
                task += 1
            elif task_time == min_time:
                worker += 1
                task_time = 0

            else:
                task_time = min_time - start
                check = False
                dura = self.tasks[task].duration - task_time
                self.__executor_schedule[worker].append(ScheduleItem(self.__tasks[task], start, task_time))
                worker += 1
                task_time = 0
        for worker_id in range(len(self.__executor_schedule)-1):
            if worker_id == len(self.__executor_schedule)-1:
                self.__executor_schedule[worker_id].append(ScheduleItem(None, 0,
                                                                 min_time,
                                                                 True))
            elif self.__executor_schedule[worker_id][-1].duration + self.__executor_schedule[worker_id][-1].start < min_time:
                self.__executor_schedule[worker_id].append(ScheduleItem(None,self.__executor_schedule[worker_id][-1].duration,min_time-self.__executor_schedule[worker_id][-1].duration,True))
        if worker != len(self.__executor_schedule) - 1:
            self.__executor_schedule[-1].append(ScheduleItem(None, 0,
                                                             min_time,
                                                             True))
        elif self.__executor_schedule[-1][-1].duration + self.__executor_schedule[-1][-1].start < min_time:
            self.__executor_schedule[-1].append(ScheduleItem(None, self.__executor_schedule[-1][-1].duration,
                                                             min_time - self.__executor_schedule[-1][-1].duration,
                                                             True))





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
    tasks = [Task('a', 1), Task('b', 1), Task('c', 10)]

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = Schedule(tasks, 3)

    # Выведем в консоль полученное расписание
    print(schedule)

    for i in range(schedule.executor_count):
        print(f'\nРасписание для исполнителя # {i + 1}:')
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)
