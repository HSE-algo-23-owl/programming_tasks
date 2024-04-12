from schedule_pack.abs_schedule import AbstractSchedule
from schedule_pack.errors import ScheduleArgumentError
from schedule_pack.staged_task import StagedTask
from schedule_pack.schedule_item import ScheduleItem
from schedule_pack.constants import ERR_TASKS_NOT_LIST_MSG, \
    ERR_TASKS_EMPTY_LIST_MSG, ERR_INVALID_TASK_TEMPL, \
    ERR_INVALID_STAGE_CNT_TEMPL


class ConveyorSchedule(AbstractSchedule):
    """Класс представляет оптимальное расписание для списка задач, состоящих
     из двух этапов и двух исполнителей. Для построения расписания используется
     алгоритм Джонсона.

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

    def __init__(self, tasks: list[StagedTask]):
        """Конструктор для инициализации объекта расписания.

        :param tasks: Список задач для составления расписания.
        :raise ScheduleArgumentError: Если список задач предоставлен в
        некорректном формате или количество этапов для какой-либо задачи не
        равно двум.
        """
        ConveyorSchedule.__validate_params(tasks)
        super().__init__(tasks, 2)

        # Процедура заполняет пустую заготовку расписания для каждого
        # исполнителя объектами ScheduleItem.
        self.__fill_schedule(ConveyorSchedule.__sort_tasks(tasks))

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._executor_schedule[0][-1].end

    def __fill_schedule(self, tasks: list[StagedTask]) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, согласно алгоритму Джонсона."""
        first_executor_schedule = self._executor_schedule[0]
        second_executor_schedule = self._executor_schedule[1]

        first_exec_time = 0

        for task in tasks:  # заполнение расписания 1-го исполнителя
            stage_duration = task.stage_duration(0)
            first_executor_schedule.append(ScheduleItem(task, first_exec_time, stage_duration))
            first_exec_time += stage_duration

        task_idx = first_task_idx = 0
        total_time = 0
        while first_task_idx < len(tasks):  # заполнение расписания 2-го исполнителя
            item = first_executor_schedule[first_task_idx]
            first_exec_task_end = item.end

            if item.task_name == tasks[task_idx].name and first_exec_task_end > total_time:
                second_executor_schedule.append(ScheduleItem(None, total_time, abs(first_exec_task_end-total_time), True))
                total_time += abs(first_exec_task_end-total_time)
            else:
                second_executor_schedule.append(ScheduleItem(tasks[task_idx], total_time, tasks[task_idx].stage_duration(1)))
                total_time += tasks[task_idx].stage_duration(1)
                task_idx += 1

            if total_time >= first_exec_task_end:
                first_task_idx += 1

        second_executor_schedule.append(ScheduleItem(tasks[-1], total_time, tasks[-1].stage_duration(1)))
        first_executor_schedule.append(ScheduleItem(None, first_executor_schedule[-1].end,
                                                    second_executor_schedule[-1].end-first_executor_schedule[-1].end,
                                                    True))

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        first_group = []
        second_group = []

        for task in tasks:
            first_stage_duration, second_stage_duration = task.stage_durations

            if first_stage_duration <= second_stage_duration:
                first_group.append(task)
            else:
                second_group.append(task)

        first_group.sort(key=lambda x: x.stage_duration(0))
        second_group.sort(key=lambda x: x.stage_duration(1), reverse=True)

        return first_group + second_group


    @staticmethod
    def __validate_params(tasks: list[StagedTask]) -> None:
        """Проводит валидацию входящих параметров для инициализации объекта
        класса ConveyorSchedule."""
        if not isinstance(tasks, list):
            raise ScheduleArgumentError(ERR_TASKS_NOT_LIST_MSG)
        if len(tasks) < 1:
            raise ScheduleArgumentError(ERR_TASKS_EMPTY_LIST_MSG)
        for idx, value in enumerate(tasks):
            if not isinstance(value, StagedTask):
                raise ScheduleArgumentError(ERR_INVALID_TASK_TEMPL.format(idx))
            if value.stage_count != 2:
                raise ScheduleArgumentError(
                    ERR_INVALID_STAGE_CNT_TEMPL.format(idx))


if __name__ == '__main__':
    print('Пример использования класса ConveyorSchedule')

    # Инициализируем входные данные для составления расписания
    tasks = [
        StagedTask('a', [7, 2]),
        StagedTask('b', [3, 4]),
        StagedTask('c', [2, 5]),
        StagedTask('d', [4, 1]),
        StagedTask('e', [6, 6]),
        StagedTask('f', [5, 3]),
        StagedTask('g', [4, 5])
    ]

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = ConveyorSchedule(tasks)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f'\nРасписание для исполнителя # {i + 1}:')
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)
