from schedule_pack import Task
from schedule_pack.errors import TaskArgumentError
from schedule_pack.constants import ERR_NOT_STR_NAME_MSG, ERR_EMPTY_NAME_MSG,\
    STAGED_TASK_STR_TEMPL, ERR_NOT_LIST_DUR_MSG, ERR_EMPTY_LIST_DUR_MSG, \
    ERR_NOT_NUMBER_DUR_TEMPL, ERR_NEG_NUMBER_DUR_TEMPL, ERR_STAGE_NOT_INT_MSG, \
    ERR_STAGE_OUT_OF_RANGE_MSG


class StagedTask(Task):
    """Представляет задачу для составления расписания. Задача состоит из
    нескольких этапов, каждый из которых имеет некоторую продолжительность.

    Properties
    ----------
    name(self) -> str:
        Возвращает название задачи.

    duration(self) -> int:
        Возвращает общую продолжительность задачи.

    stage_count(self) -> int:
        Возвращает количество этапов задачи.

    stage_duration(self, stage_idx: int) -> int | float:
        Возвращает продолжительность этапа задачи.
    """
    def __init__(self, name: str, stage_durations: list[int | float]):
        """Конструктор для создания задачи.

        :param name: Название задачи.
        :param stage_durations: Продолжительности этапов задачи.
        :raise TaskArgumentException: Если название задачи не является строкой,
        если продолжительность этапов не является списком, список пуст или
        продолжительность какого либо этапа не является числом, либо меньше
        или равна нулю.
        """
        StagedTask.__validate_params(name, stage_durations)
        super().__init__(name, sum(stage_durations))
        self._stage_durations = stage_durations

    def __str__(self):
        return STAGED_TASK_STR_TEMPL.format(self._name, self._duration,
                                            self.stage_count)

    def __eq__(self, other):
        if not isinstance(other, StagedTask):
            return False
        if other.name != self.name:
            return False
        if other.stage_count != self.stage_count:
            return False
        for other_dur, self_dur in zip(other.stage_durations,
                                       self.stage_durations):
            if other_dur != self_dur:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.name, self.stage_durations))

    @property
    def stage_count(self) -> int:
        """Возвращает количество этапов задачи."""
        return len(self._stage_durations)

    @property
    def stage_durations(self) -> tuple[int | float]:
        """Возвращает продолжительность этапов задачи."""
        return tuple(self._stage_durations)

    def stage_duration(self, stage_idx: int) -> int | float:
        """Возвращает продолжительность этапа задачи."""
        self.__validate_stage_idx(stage_idx)
        return self._stage_durations[stage_idx]

    @staticmethod
    def __validate_params(name: str, stage_durations: list[int | float]) \
            -> None:
        """Проверяет корректность переданных параметров."""
        if not isinstance(name, str):
            raise TaskArgumentError(ERR_NOT_STR_NAME_MSG)
        if len(name) < 1:
            raise TaskArgumentError(ERR_EMPTY_NAME_MSG)
        if not isinstance(stage_durations, list):
            raise TaskArgumentError(ERR_NOT_LIST_DUR_MSG)
        if len(stage_durations) == 0:
            raise TaskArgumentError(ERR_EMPTY_LIST_DUR_MSG)
        for idx, duration in enumerate(stage_durations):
            if not isinstance(duration, (int, float)):
                raise TaskArgumentError(ERR_NOT_NUMBER_DUR_TEMPL.format(idx))
            if duration <= 0:
                raise TaskArgumentError(ERR_NEG_NUMBER_DUR_TEMPL.format(idx))

    def __validate_stage_idx(self, stage_idx: int) -> None:
        """Проводит валидацию индекса этапа."""
        if not isinstance(stage_idx, int) or stage_idx < 0:
            raise TaskArgumentError(ERR_STAGE_NOT_INT_MSG)
        if stage_idx >= self.stage_count:
            raise TaskArgumentError(ERR_STAGE_OUT_OF_RANGE_MSG)


if __name__ == '__main__':
    print('Пример использования класса StagedTask\n')

    # Инициализируем экземпляр класса Task
    task = StagedTask('sample task', [1, 2, 3])

    # Контроль корректности входных данных
    try:
        StagedTask('wrong task', [-1])
    except TaskArgumentError as error:
        print(f'Ошибка инициализации: {error}')

    # Приведение экземпляра класса StagedTask к строковому типу
    print(task)

    for idx in range(task.stage_count):
        print(f'Этап {idx} продолжительность {task.stage_duration(idx)}')
