"""Классы пакета Расписание.

Task: Представляет задачу для составления расписания.

ScheduleItem: Представляет собой элемент расписания, включает в себя
задачу, выполняющуюся в течение некоторого времени.

Schedule: Представляет оптимальное расписание для списка задач и количества
исполнителей. Для построения расписания используется Ленточная стратегия.
"""


from schedule_pack.task import Task
from schedule_pack.schedule_item import ScheduleItem
from schedule_pack.schedule import Schedule


__all__ = ['Task', 'ScheduleItem', 'Schedule']
__version__ = '1.0.0'
__author__ = 'Alexander Mikhailov'
__license__ = 'MIT'
