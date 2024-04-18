from schedule_pack.errors.schedule_error import ScheduleError


class ScheduleItemError(ScheduleError):
    """Ошибка некорректного параметра инициализации элемента расписания.
    Attributes:
        message -- Сообщение об ошибке.
    """

    def __init__(self, message):
        super().__init__(message)
