import re
import unittest
import networkx as nx

from graph_pack.graph_generator import GraphGenerator, \
    ERR_NOT_INT_TREE_CNT, ERR_LESS_THAN_1_TREE_CNT, ERR_NOT_INT_VERTEX_CNT, \
    ERR_LESS_THAN_1_VERTEX_CNT, ERR_VERTEX_CNT_LESS_THAN_TREE_CNT, CHARS


COLOR = 'color'


class TestGraphGenerator(unittest.TestCase):
    def __check_color_cnt(self, graph: nx.DiGraph, tree_cnt):
        """Проверяет соответствие количества цветов вершин количеству
        деревьев в графе."""
        color_set = set()
        for node_name in list(graph.nodes.keys()):
            if COLOR not in graph.nodes[node_name]:
                return False
            color_set.add(graph.nodes[node_name][COLOR])
        return len(color_set) == tree_cnt

    def __check_vertex_names(self, graph: nx.DiGraph):
        """Проверяет корректность наименования вершин графа."""
        pattern = f'^[{CHARS}]+$'
        for node_name in list(graph.nodes.keys()):
            if not re.match(pattern, node_name):
                return False
        return True

    def test_not_int_tree_cnt(self):
        """Проверяет выброс исключения при передаче нечислового значения
        количества деревьев."""
        incorrect_val = [1.1, None, 'str', []]
        for val in incorrect_val:
            with self.assertRaises(TypeError) as error:
                GraphGenerator.generate_random_forest(val, 1)
            self.assertEqual(ERR_NOT_INT_TREE_CNT, str(error.exception))

    def test_less_than_1_tree_cnt(self):
        """Проверяет выброс исключения при передаче некорректного значения
        количества деревьев."""
        incorrect_val = [-1, 0]
        for val in incorrect_val:
            with self.assertRaises(ValueError) as error:
                GraphGenerator.generate_random_forest(val, 1)
            self.assertEqual(ERR_LESS_THAN_1_TREE_CNT, str(error.exception))

    def test_not_int_vertex_cnt(self):
        """Проверяет выброс исключения при передаче нечислового значения
        количества вершин."""
        incorrect_val = [1.1, None, 'str', []]
        for val in incorrect_val:
            with self.assertRaises(TypeError) as error:
                GraphGenerator.generate_random_forest(1, val)
            self.assertEqual(ERR_NOT_INT_VERTEX_CNT, str(error.exception))

    def test_less_than_1_vertex_cnt(self):
        """Проверяет выброс исключения при передаче некорректного значения
        количества вершин."""
        incorrect_val = [-1, 0]
        for val in incorrect_val:
            with self.assertRaises(ValueError) as error:
                GraphGenerator.generate_random_forest(1, val)
            self.assertEqual(ERR_LESS_THAN_1_VERTEX_CNT, str(error.exception))

    def test_vertex_cnt_less_than_tree_cnt(self):
        """Проверяет выброс исключения при передаче некорректного значения
        количества вершин меньшего чем значение количества деревьев."""
        with self.assertRaises(ValueError) as error:
            GraphGenerator.generate_random_forest(2, 1)
        self.assertEqual(ERR_VERTEX_CNT_LESS_THAN_TREE_CNT,
                         str(error.exception))

    def test_tree1_vertex1(self):
        """Проверяет генерацию графа с одной вершиной."""
        graph = GraphGenerator.generate_random_forest(1, 1)
        self.assertEqual(1, graph.order())

    def test_tree1_vertex2(self):
        """Проверяет генерацию графа с одним деревом и двумя вершинами."""
        graph = GraphGenerator.generate_random_forest(1, 2)
        self.assertEqual(2, graph.order())
        self.assertEqual(1, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 1))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_tree1_vertex3(self):
        """Проверяет генерацию графа с одним деревом и тремя вершинами."""
        graph = GraphGenerator.generate_random_forest(1, 3)
        self.assertEqual(3, graph.order())
        self.assertEqual(2, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 1))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_tree2_vertex2(self):
        """Проверяет генерацию графа с двумя деревьями и двумя вершинами."""
        graph = GraphGenerator.generate_random_forest(2, 2)
        self.assertEqual(2, graph.order())
        self.assertEqual(0, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 2))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_tree2_vertex3(self):
        """Проверяет генерацию графа с двумя деревьями и тремя вершинами."""
        graph = GraphGenerator.generate_random_forest(2, 3)
        self.assertEqual(3, graph.order())
        self.assertEqual(1, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 2))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_tree3_vertex3(self):
        """Проверяет генерацию графа с тремя деревьями и тремя вершинами."""
        graph = GraphGenerator.generate_random_forest(3, 3)
        self.assertEqual(3, graph.order())
        self.assertEqual(0, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 3))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_tree3_vertex4(self):
        """Проверяет генерацию графа с тремя деревьями и четырьмя вершинами."""
        graph = GraphGenerator.generate_random_forest(3, 4)
        self.assertEqual(4, graph.order())
        self.assertEqual(1, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 3))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_tree3_vertex5(self):
        """Проверяет генерацию графа с тремя деревьями и пятью вершинами."""
        graph = GraphGenerator.generate_random_forest(3, 5)
        self.assertEqual(5, graph.order())
        self.assertEqual(2, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 3))
        self.assertTrue(self.__check_vertex_names(graph))

    def test_tree3_vertex6(self):
        """Проверяет генерацию графа с тремя деревьями и шестью вершинами."""
        graph = GraphGenerator.generate_random_forest(3, 6)
        self.assertEqual(6, graph.order())
        self.assertEqual(3, len(graph.edges))
        self.assertTrue(self.__check_color_cnt(graph, 3))
        self.assertTrue(self.__check_vertex_names(graph))


if __name__ == '__main__':
    unittest.main()
