import heapq


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(graph, start, goal):
    if not isinstance(start, tuple) or not isinstance(goal, tuple):
        raise ValueError("Start and goal must be tuples representing coordinates.")

    if len(start) != 2 or len(goal) != 2:
        raise ValueError("Start and goal tuples must have exactly two elements.")

    if not graph.in_bounds(start) or not graph.in_bounds(goal):
        raise ValueError("Start or goal is out of bounds.")

    if not graph.passable(start) or not graph.passable(goal):
        raise ValueError("Start or goal is on an obstacle.")

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in graph.get_neighbors(current):
            tentative_g_score = g_score[current] + graph.cost(current, neighbor)

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


class GridWithWeights:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.weights = {}

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def get_neighbors(self, id):
        (x, y) = id
        neighbors = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)
