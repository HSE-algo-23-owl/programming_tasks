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

        first_worker, second_worker = self._executor_schedule[0], self._executor_schedule[1]
        first_time, second_time = 0, 0
        for i in tasks:
            first_worker.append(ScheduleItem(i, first_time, i.stage_duration(0)))
            first_time += i.stage_duration(0)
            if not second_worker:
                second_worker.append(ScheduleItem(None, second_time, i.stage_duration(0), True))
                second_time += i.stage_duration(0)
                second_worker.append(ScheduleItem(i, second_time, i.stage_duration(1)))
                second_time += i.stage_duration(1)
            elif second_time < first_time:
                second_worker.append(ScheduleItem(None,second_time, first_time - second_time, True))
                second_time += first_time - second_time
                second_worker.append(ScheduleItem(i, second_time, i.stage_duration(1)))
                second_time += i.stage_duration(1)
            else:
                second_worker.append(ScheduleItem(i,second_time,i.stage_duration(1)))
                second_time += i.stage_duration(1)
        first_worker.append(ScheduleItem(None,first_time,second_time-first_time,True))

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        first_group, second_group = [], []
        for i in tasks:
            if i.stage_duration(0) <= i.stage_duration(1):
                first_group.append(i)
            else:
                second_group.append(i)
        def item_sort_by_first(i):
            return i.stage_duration(0)
        def item_sort_by_second(i):
            return i.stage_duration(1)

        first_group.sort(key=item_sort_by_first)
        second_group.sort(key=item_sort_by_second, reverse=True)
        sorted_tasks = []
        for i in first_group:
            sorted_tasks.append(i)
        for i in second_group:
            sorted_tasks.append(i)
        return sorted_tasks


        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        pass

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
        StagedTask('a', [1, 1]),
        StagedTask('b', [1, 1])]

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = ConveyorSchedule(tasks)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f'\nРасписание для исполнителя # {i + 1}:')
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)
