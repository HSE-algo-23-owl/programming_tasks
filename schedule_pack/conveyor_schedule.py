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
        current_finish_time, job_index, last_finished_job_index, machine_b_finish_time = 0, 0, 0, 0
        num1 = self._executor_schedule[0]
        for index, job in enumerate(tasks):
            num1.append(ScheduleItem(job, current_finish_time, job.stage_duration(0)))
            current_finish_time += job.stage_duration(0)
        while last_finished_job_index < len(tasks):
            if num1[last_finished_job_index].end <= machine_b_finish_time or num1[last_finished_job_index].task_name != tasks[job_index].name:
                self._executor_schedule[1].append(
                    ScheduleItem(tasks[job_index], machine_b_finish_time, tasks[job_index].stage_duration(1)))
                machine_b_finish_time += tasks[job_index].stage_duration(1)
                job_index += 1
            else:
                self._executor_schedule[1].append(
                    ScheduleItem(None, machine_b_finish_time,
                                 abs(num1[last_finished_job_index].end - machine_b_finish_time),
                                 True))
                machine_b_finish_time += abs(
                    num1[last_finished_job_index].end - machine_b_finish_time)

            if not(machine_b_finish_time < num1[last_finished_job_index].end):
                last_finished_job_index += 1

        self._executor_schedule[1].append(ScheduleItem(tasks[-1], machine_b_finish_time, tasks[-1].stage_duration(1)))
        num1.append(ScheduleItem(None, num1[-1].end,
                                                       self._executor_schedule[1][-1].end - num1[
                                                           -1].end, True))

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        group_A = []
        group_B = []
        for item in tasks:
            if item.stage_duration(0) <= item.stage_duration(1):
                group_A.append(item)
            else:
                group_B.append(item)

        def first_sort(item):
            return item.stage_duration(0)

        def second_sort(item):
            return item.stage_duration(1)

        temp_array = []
        group_B.sort(key=second_sort, reverse=True)
        group_A.sort(key=first_sort)
        for item in group_A:
            temp_array.append(item)
        for item in group_B:
            temp_array.append(item)
        return temp_array

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
