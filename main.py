from schedule_pack import StagedTask, ConveyorSchedule

"""Для решения задачи составления оптимального расписания с использованием 
алгоритма Джонсона подготовлен python-пакет schedule_pack.

В пакете представлены следующие классы
    - StagedTask: Представляет задачу для составления расписания. Используется в
    качестве входных данных для класса Schedule.
    - ConveyorSchedule: Представляет оптимальное расписание для списка задач и
     двух исполнителей. Для построения расписания используется алгоритм 
     Джонсона. Для каждого исполнителя расписание представлено набором
     экземпляров класса ScheduleItem.
    - ScheduleItem: Представляет собой элемент расписания, включает в себя
    задачу, выполняющуюся в течение некоторого времени, с указанием моментов
    начала и окончания ее выполнения.

!!! Для выполнения задания необходимо реализовать два приватных метода 
класса Schedule, расположенного в файле schedule_pack/conveyor_schedule.py:
    - __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]: Возвращает
    отсортированный список задач для применения алгоритма Джонсона.
    - __fill_schedule(self, tasks: list[StagedTask]) -> None: Процедура
    составляет расписание из элементов ScheduleItem для каждого исполнителя,
    согласно алгоритму Джонсона.
Указанные методы используются при инициализации объекта класса ConveyorSchedule 
в методе __init__.

Проверить реализацию класса Schedule можно запустив набор авто-тестов 
в файле schedule_pack/tests/test_conveyor_schedule.py.

Запустить тесты для проверки всего пакета schedule_pack можно с помощью 
файла test_runner.py.

"""


def main():
    print('Пример использования класса ConveyorSchedule')

    # Инициализируем входные данные для составления расписания
    tasks = [
        StagedTask('a', [7, 2]),
        StagedTask('b', [3, 4]),
        StagedTask('c', [2, 5]),
        StagedTask('d', [4, 1]),
        StagedTask('e', [6, 6]),
        StagedTask('f', [5, 3]),
        StagedTask('g', [4, 5])
    ]

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = ConveyorSchedule(tasks)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f'\nРасписание для исполнителя # {i + 1}:')
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)


if __name__ == '__main__':
    main()
