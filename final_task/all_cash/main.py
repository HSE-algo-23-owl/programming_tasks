from typing import List, Any

INF = 99999  # Если нет пути
PARAM_ERR_MSG = ('Таблица расстояний не является квадратной матрицей с '
                 'числовыми значениями')


def floydWarshall(graph: list[list[int]]) -> list[list[list[int]], bool]:
    """Применяется алгоритм Флойда–Уоршелла для поиска кратчайших путей от каждой вершины к каждой вершине.
    :param graph - матрица смежности расстояний в графе.
    :return dist - матрица минимальных расстояний между вершинами.
    :return check_negative_cycle(graph) - возвращает True, если в графе есть отрицательные циклы, False в ином случае
    """

    validate(graph)
    dist = list(map(lambda i: list(map(lambda j: j, i)), graph))
    peak = len(graph)

    for k in range(peak):
        for i in range(peak):
            for j in range(peak):
                without_peak = dist[i][j]
                if dist[i][k] == INF or dist[k][j] == INF:
                    with_peak = INF
                else:
                    with_peak = dist[i][k] + dist[k][j]
                dist[i][j] = min(without_peak, with_peak)
    return [dist, check_negative_cycle(dist)]


def validate(graph: list[list[int]]):
    if not isinstance(graph, list) or not graph:
        raise TypeError(PARAM_ERR_MSG)
    for i in range(len(graph)):
        if len(graph[i]) != len(graph):
            raise TypeError(PARAM_ERR_MSG)
    for row in graph:
        for cell in row:
            if not (isinstance(cell, int) or cell is None):
                raise TypeError(PARAM_ERR_MSG)

    pass


def check_negative_cycle(graph : list[list[int]]) -> bool:
    for i in range(len(graph)):
        if graph[i][i] < 0:
            return True
    return False


def printSolution(dist) -> None:
    for row in dist:
        for element in row:
            if element == INF:
                print(f"{'  ∞':3}", end="")  # Форматируем вывод с отступом
            else:
                print(f"{element:3}", end="")
        print()


if __name__ == "__main__":
    graph = [[0, 5, INF, 10],
                  [INF, 0, 3, INF],
                  [INF, INF, 0, 1],
                  [INF, INF, INF, 0]
                  ]

    result = floydWarshall(graph)
    print("Матрица кратчайших расстояний:")
    printSolution(result[0])
    print(result[0])
    print(f"Содержит ли граф циклы отрицательной длины: {result[1]}")
