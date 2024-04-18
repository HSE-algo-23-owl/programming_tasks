from schedule_pack.errors.schedule_item_error import ScheduleItemError
from schedule_pack.task import Task
from schedule_pack.constants import ERR_NOT_NONE_TASK_MSG, ERR_NONE_TASK_MSG, \
    ERR_START_NOT_NUMBER_MSG, ERR_START_NEG_NUMBER_MSG, \
    ERR_DUR_NOT_NUMBER_MSG, ERR_DUR_NOT_POS_NUMBER_MSG, \
    SCHEDULE_ITEM_STR_TEMPL, SCHEDULE_ITEM_DOWNTIME_STR_TEMPL


class ScheduleItem:
    """Класс представляет собой элемент расписания, включает в себя задачу,
    выполняющуюся в течение некоторого времени.

    Properties
    ----------
    task_name(self) -> str:
        Возвращает название выполняемой задачи или downtime если указан
        признак простоя.

    is_downtime(self) -> bool:
        Возвращает значение признака простоя.

    start(self) -> float:
        Возвращает момент начала выполнения задачи.

    duration(self) -> float:
        Возвращает продолжительность выполнения задачи.

    end(self) -> float:
        Возвращает момент окончания выполнения задачи.
    """
    def __init__(self, task: Task | None, start: float,
                 duration: float, is_downtime: bool = False):
        """Метод инициализации объекта класса.

        :param task: Выполняемая задача.
        :param start: Начало выполнения задачи.
        :param duration: Продолжительность выполнения задачи.
        :param is_downtime: Признак простоя.
        :raise ScheduleArgumentException: Если не указана задача и признак
            простоя, если указаны некорректные значения начала и
            продолжительности выполнения задачи.
        """
        ScheduleItem.__validate_params(task, start, duration, is_downtime)
        self.__task = task
        self.__start = start
        self.__duration = duration
        self.__is_downtime = is_downtime

    @property
    def task_name(self) -> str:
        """Возвращает название выполняемой задачи или downtime если указан
        признак простоя."""
        return 'downtime' if self.__is_downtime else self.__task.name

    @property
    def is_downtime(self) -> bool:
        """Возвращает значение признака простоя."""
        return self.__is_downtime

    @property
    def start(self) -> float:
        """Возвращает момент начала выполнения задачи."""
        return self.__start

    @property
    def duration(self) -> float:
        """Возвращает продолжительность выполнения задачи."""
        return self.__duration

    @property
    def end(self) -> float:
        """Возвращает момент окончания выполнения задачи."""
        return self.__start + self.__duration

    def __str__(self):
        if self.__is_downtime:
            return SCHEDULE_ITEM_DOWNTIME_STR_TEMPL.format(self.start, self.end)
        return SCHEDULE_ITEM_STR_TEMPL.format(self.task_name, self.start,
                                              self.end)

    def __eq__(self, other):
        return (self.__task == other.__task and self.start == other.start
                and self.duration == other.duration)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.__task, self.start, self.duration))

    @staticmethod
    def __validate_params(task: Task | None, start: float, duration: float,
                          is_downtime: bool) -> None:
        """Проверяет корректность входных данных для создания экземпляра
        класса."""
        if is_downtime and task is not None:
            raise ScheduleItemError(ERR_NOT_NONE_TASK_MSG)
        if not isinstance(task, Task) and not is_downtime:
            raise ScheduleItemError(ERR_NONE_TASK_MSG)
        if not isinstance(start, int) and not isinstance(start, float):
            raise ScheduleItemError(ERR_START_NOT_NUMBER_MSG)
        if start < 0:
            raise ScheduleItemError(ERR_START_NEG_NUMBER_MSG)
        if not isinstance(duration, int) and not isinstance(duration, float):
            raise ScheduleItemError(ERR_DUR_NOT_NUMBER_MSG)
        if duration <= 0:
            raise ScheduleItemError(ERR_DUR_NOT_POS_NUMBER_MSG)


if __name__ == '__main__':
    print('Пример использования класса ScheduleItem\n')

    # Инициализируем экземпляр класса ScheduleItem
    task = Task('task 1', 1.1)
    schedule_item = ScheduleItem(task, 0, 1)

    # Контроль корректности входных данных
    try:
        ScheduleItem(task, -1, 1)
    except ScheduleItemError as error:
        print(f'Ошибка инициализации: {error}')

    # Приведение экземпляра класса ScheduleItem к строковому типу
    print(schedule_item)
