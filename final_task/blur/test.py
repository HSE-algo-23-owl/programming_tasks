import unittest
from main import bfs, ERROR_START_NODE_NOT_IN_GRAPH, ERROR_EMPTY_GRAPH

class Test(unittest.TestCase):
    """Это будет класс для тестирования разработанного алгоритма"""

    def test_something(self):
        """Здесь будут тест кейсы тестирования разработанного алгоритма"""
        self.assertEqual(1, 1)

    def test_empty_graph(self): #сделано
        graph = {}
        start = 'A'
        with self.assertRaises(ValueError) as err:
            bfs(graph, start)
        self.assertEqual(ERROR_EMPTY_GRAPH, str(err.exception))

    def test_single_node_graph(self):
        graph = {'A': []}
        start = 'A'
        self.assertEqual(bfs(graph, start), ['A'])

    def test_graph_without_edges(self):
        graph = {'A': [], 'B': [], 'C': []}
        start = 'A'
        self.assertEqual(bfs(graph, start), ['A'])

    def test_graph_with_cycles(self):
        graph = {
            'A': ['B', 'C'],
            'B': ['A', 'D', 'E'],
            'C': ['A', 'F'],
            'D': ['B'],
            'E': ['B', 'F'],
            'F': ['C', 'E']
        }
        start = 'A'
        self.assertEqual(bfs(graph, start), ['A', 'B', 'C', 'D', 'E', 'F'])

    def test_graph_with_custom_data(self):
        graph = {
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['E'],
            'D': ['F'],
            'E': ['F'],
            'F': []
        }
        start = 'A'
        self.assertEqual(bfs(graph, start), ['A', 'B', 'C', 'D', 'E', 'F'])

    def test_order_of_nodes(self):
        graph = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': [],
            'E': ['F'],
            'F': []
        }
        start = 'A'
        self.assertEqual(bfs(graph, start), ['A', 'B', 'C', 'D', 'E', 'F'])

    def test_graph_is_none(self):
        graph = None
        start = 'A'
        with self.assertRaises(ValueError):
            bfs(graph, start)

    def test_start_node_not_in_graph(self):
        graph = {
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['E'],
            'D': ['F'],
            'E': ['F'],
            'F': []
        }
        start = 'G'
        with self.assertRaises(ValueError) as err:
            bfs(graph, start)
        self.assertEqual(ERROR_START_NODE_NOT_IN_GRAPH, str(err.exception))

if __name__ == '__main__':
    unittest.main()
