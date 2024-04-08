class ScheduleError(Exception):
    """Общая ошибка пакета Расписание.
    Attributes:
        message -- Сообщение об ошибке.
    """

    def __init__(self, message):
        super().__init__(message)
