from schedule_pack.errors import TaskArgumentError
from schedule_pack.constants import ERR_NOT_STR_NAME_MSG, ERR_EMPTY_NAME_MSG,\
    ERR_NOT_NUMBER_DUR_MSG, ERR_NEG_NUMBER_DUR_MSG, TASK_STR_TEMPL


class Task:
    """Представляет задачу для составления расписания.

    Properties
    ----------
    name(self) -> str:
        Возвращает название задачи.

    duration(self) -> int:
        Возвращает продолжительность задачи.
    """
    def __init__(self, name: str, duration: int | float):
        """Конструктор для создания задачи.

        :param name: Название задачи.
        :param duration: Продолжительность задачи.
        :raise TaskArgumentException: Если название задачи не является строкой,
        если продолжительность не является числом, либо меньше или равно нулю.
        """
        Task.__validate_params(name, duration)
        self._name: str = name
        self._duration: int | float = duration

    def __str__(self):
        return TASK_STR_TEMPL.format(self._name, self._duration)

    def __eq__(self, other):
        return (other and self.name == other.name
                and self.duration == other.duration)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.name, self.duration))

    @property
    def name(self) -> str:
        """Возвращает название задачи."""
        return self._name

    @property
    def duration(self) -> int | float:
        """Возвращает продолжительность задачи."""
        return self._duration

    @staticmethod
    def __validate_params(name: str, duration: int | float) -> None:
        """Проверяет корректность переданных параметров."""
        if not isinstance(name, str):
            raise TaskArgumentError(ERR_NOT_STR_NAME_MSG)
        if len(name) < 1:
            raise TaskArgumentError(ERR_EMPTY_NAME_MSG)
        if not isinstance(duration, int) and not isinstance(duration, float):
            raise TaskArgumentError(ERR_NOT_NUMBER_DUR_MSG)
        if duration <= 0:
            raise TaskArgumentError(ERR_NEG_NUMBER_DUR_MSG)


if __name__ == '__main__':
    print('Пример использования класса Task\n')

    # Инициализируем экземпляр класса Task
    task = Task('task 1', 1.1)

    # Контроль корректности входных данных
    try:
        Task('task 1', -1)
    except TaskArgumentError as error:
        print(f'Ошибка инициализации: {error}')

    # Приведение экземпляра класса Task к строковому типу
    print(task)
