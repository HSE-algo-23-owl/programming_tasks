"""Классы ошибок пакета Расписание.

ScheduleError: Общая ошибка пакета Расписание.

ScheduleArgumentError: Ошибка некорректного параметра при инициализации
расписания.

ScheduleItemError: Ошибка некорректного параметра инициализации элемента
расписания.

TaskArgumentError: Ошибка некорректного параметра инициализации задачи.

"""

from schedule_pack.errors.schedule_error import ScheduleError
from schedule_pack.errors.schedule_argument_error import ScheduleArgumentError
from schedule_pack.errors.schedule_item_error import ScheduleItemError
from schedule_pack.errors.task_argument_error import TaskArgumentError


__all__ = ['ScheduleError', 'ScheduleArgumentError', 'ScheduleItemError',
           'TaskArgumentError']
