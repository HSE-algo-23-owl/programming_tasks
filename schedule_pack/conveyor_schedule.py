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
        primary_schedule = self._executor_schedule[0]
        auxiliary_schedule = self._executor_schedule[1]

        start_time = 0

        for activity in tasks:
            phase_length = activity.stage_duration(0)
            primary_schedule.append(ScheduleItem(activity, start_time, phase_length))
            start_time += phase_length

        current_task_index = next_task_index = 0
        cumulative_time = 0

        while next_task_index < len(tasks):
            schedule_entry = primary_schedule[next_task_index]
            completion_time = schedule_entry.end

            if schedule_entry.task_name == tasks[current_task_index].name and completion_time > cumulative_time:
                idle_duration = abs(completion_time - cumulative_time)
                auxiliary_schedule.append(ScheduleItem(None, cumulative_time, idle_duration, True))
                cumulative_time += idle_duration
            else:
                task_duration = tasks[current_task_index].stage_duration(1)
                auxiliary_schedule.append(ScheduleItem(tasks[current_task_index], cumulative_time, task_duration))
                cumulative_time += task_duration
                current_task_index += 1

            if cumulative_time >= completion_time:
                next_task_index += 1

        final_task = tasks[-1]
        auxiliary_schedule.append(ScheduleItem(final_task, cumulative_time, final_task.stage_duration(1)))
        primary_schedule.append(ScheduleItem(None, primary_schedule[-1].end,
                                             auxiliary_schedule[-1].end - primary_schedule[-1].end, True))

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        primary_tasks = []
        secondary_tasks = []

        for item in tasks:
            initial_duration, later_duration = item.stage_durations

            if initial_duration <= later_duration:
                primary_tasks.append(item)
            else:
                secondary_tasks.append(item)

        primary_tasks.sort(key=lambda task: task.stage_duration(0))
        secondary_tasks.sort(key=lambda task: task.stage_duration(1), reverse=True)

        sorted_tasks = primary_tasks + secondary_tasks
        return sorted_tasks

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
