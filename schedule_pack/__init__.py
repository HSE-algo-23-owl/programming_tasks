"""Классы пакета Расписание.

Task: Представляет задачу для составления расписания.

ScheduleItem: Представляет собой элемент расписания, включает в себя
задачу, выполняющуюся в течение некоторого времени.

Schedule: Представляет оптимальное расписание для списка задач и количества
исполнителей. Для построения расписания используется Ленточная стратегия.

LevelSchedule: Класс представляет оптимальное расписание для списка задач.
Все задачи единичной длительности и могут зависеть друг от друга. Для
построения расписания используется уровневая стратегия.
"""


from schedule_pack.task import Task
from schedule_pack.schedule_item import ScheduleItem
from schedule_pack.schedule import Schedule
from schedule_pack.level_schedule import LevelSchedule


__all__ = ['Task', 'ScheduleItem', 'Schedule', 'LevelSchedule']
__version__ = '1.0.0'
__author__ = 'Alexander Mikhailov'
__license__ = 'MIT'
