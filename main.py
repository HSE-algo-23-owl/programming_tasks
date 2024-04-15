import networkx as nx

from graph_pack import GraphGenerator, GraphValidator
from schedule_pack import LevelSchedule


def main():
    print('Пример использования класса GraphGenerator')

    graph = GraphGenerator.generate_random_forest(3, 18)
    GraphGenerator.show_plot(graph)

    print('Пример использования класса GraphValidator')
    matrix = nx.adjacency_matrix(graph).toarray()
    print('Матрица смежности для графа:')
    print(matrix)
    print('Граф является обратно ориентированным деревом/лесом:',
          GraphValidator.is_inverted_trees(graph))
    print('Количество деревьев в графе:',
          GraphValidator.get_tree_count(graph))
    print('Граф содержит петли:',
          GraphValidator.graph_has_loop(graph))

    print('Пример использования класса LevelSchedule')

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = LevelSchedule(graph, 4)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f'\nРасписание для исполнителя # {i + 1}:')
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)


if __name__ == '__main__':
    main()
