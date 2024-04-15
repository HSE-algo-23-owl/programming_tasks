from schedule_pack.errors.schedule_error import ScheduleError


class ScheduleArgumentError(ScheduleError):
    """Ошибка некорректного параметра при инициализации расписания.
    Attributes:
        message -- Сообщение об ошибке.
    """

    def __init__(self, message):
        super().__init__(message)
