from schedule_pack.errors.schedule_error import ScheduleError


class TaskArgumentError(ScheduleError):
    """Ошибка некорректного параметра инициализации задачи.
    Attributes:
        message -- Сообщение об ошибке.
    """

    def __init__(self, message):
        super().__init__(message)
