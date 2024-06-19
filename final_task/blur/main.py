from collections import deque

ERROR_EMPTY_GRAPH = 'Граф пустой'
ERROR_START_NODE_NOT_IN_GRAPH = 'Стартовая вершина не находится в графе'


def bfs(graph, start):
    if not graph:
        raise ValueError(ERROR_EMPTY_GRAPH)
    if start not in graph:
        raise ValueError(ERROR_START_NODE_NOT_IN_GRAPH)

    visited = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            for neighbour in graph[node]:
                if neighbour not in visited:
                    queue.append(neighbour)

    return visited


def main():
    graph = {'A': ['B', 'C'],
             'B': ['A', 'D', 'E'],
             'C': ['A', 'B', 'E'],
             'D': ['B'],
             'E': ['B', 'C']
             }
    start = 'B'
    print(bfs(graph, start))


if __name__ == '__main__':
    main()
