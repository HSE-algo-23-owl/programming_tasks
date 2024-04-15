import unittest
import networkx as nx

from graph_pack.graph_validator import GraphValidator, \
    ERR_GRAPH_IS_NOT_INV_TREE


class TestGraphValidator(unittest.TestCase):
    graph = nx.DiGraph()

    def setUp(self):
        self.graph = nx.DiGraph()

    def test_is_inverted_trees_1tree_1node(self):
        """Проверка обратно ориентированного дерева из одной вершины."""
        self.graph.add_nodes_from(['a'])
        self.assertTrue(GraphValidator.is_inverted_trees(self.graph))

    def test_get_tree_count_1tree(self):
        """Проверка подсчета деревьев для одного дерева."""
        self.graph.add_nodes_from(['a'])
        self.assertEqual(1, GraphValidator.get_tree_count(self.graph))

    def test_graph_has_loop_1tree_1node(self):
        """Проверка отсутствия цикла для дерева из одной вершины."""
        self.graph.add_nodes_from(['a'])
        self.assertFalse(GraphValidator.graph_has_loop(self.graph))

    def test_is_inverted_trees_1tree_2node(self):
        """Проверка обратно ориентированного дерева из двух вершин."""
        self.graph.add_nodes_from(['a', 'b'])
        self.graph.add_edges_from([('b', 'a')])
        self.assertTrue(GraphValidator.is_inverted_trees(self.graph))

    def test_is_inverted_trees_1tree_3node(self):
        """Проверка обратно ориентированного дерева из трех вершин."""
        self.graph.add_nodes_from(['a', 'b', 'c'])
        self.graph.add_edges_from([('c', 'a'), ('b', 'a')])
        self.assertTrue(GraphValidator.is_inverted_trees(self.graph))

    def test_is_inverted_trees_2tree_2node(self):
        """Проверка леса обратно ориентированных деревьев, два дерева,
        две вершины."""
        self.graph.add_nodes_from(['a', 'b'])
        self.assertTrue(GraphValidator.is_inverted_trees(self.graph))

    def test_get_tree_count_2tree(self):
        """Проверка подсчета деревьев для двух деревьев."""
        self.graph.add_nodes_from(['a', 'b'])
        self.assertEqual(2, GraphValidator.get_tree_count(self.graph))

    def test_is_inverted_trees_2tree_5node(self):
        """Проверка леса обратно ориентированных деревьев, два дерева,
        пять вершин."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e'])
        self.graph.add_edges_from([('c', 'a'), ('b', 'a'), ('e', 'd')])
        self.assertTrue(GraphValidator.is_inverted_trees(self.graph))

    def test_graph_has_loop_2tree_5node(self):
        """Проверка отсутствия цикла, два дерева, пять вершин."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e'])
        self.graph.add_edges_from([('c', 'a'), ('b', 'a'), ('e', 'd')])
        self.assertFalse(GraphValidator.graph_has_loop(self.graph))

    def test_is_inverted_trees_3tree_13node(self):
        """Проверка леса обратно ориентированных деревьев, три дерева,
        тринадцать вершин."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                                   'j', 'k', 'l', 'm'])
        self.graph.add_edges_from([('d', 'a'), ('j', 'd'), ('e', 'b'),
                                   ('f', 'b'), ('k', 'e'), ('g', 'c'),
                                   ('h', 'c'), ('i', 'c'), ('l', 'g'),
                                   ('m', 'g')])
        self.assertTrue(GraphValidator.is_inverted_trees(self.graph))

    def test_get_tree_count_3tree(self):
        """Проверка подсчета деревьев для трех деревьев."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                                   'j', 'k', 'l', 'm'])
        self.graph.add_edges_from([('d', 'a'), ('j', 'd'), ('e', 'b'),
                                   ('f', 'b'), ('k', 'e'), ('g', 'c'),
                                   ('h', 'c'), ('i', 'c'), ('l', 'g'),
                                   ('m', 'g')])
        self.assertEqual(3, GraphValidator.get_tree_count(self.graph))

    def test_graph_has_loop_3tree_13node(self):
        """Проверка отсутствия цикла, три дерева, тринадцать вершин."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                                   'j', 'k', 'l', 'm'])
        self.graph.add_edges_from([('d', 'a'), ('j', 'd'), ('e', 'b'),
                                   ('f', 'b'), ('k', 'e'), ('g', 'c'),
                                   ('h', 'c'), ('i', 'c'), ('l', 'g'),
                                   ('m', 'g')])
        self.assertFalse(GraphValidator.graph_has_loop(self.graph))

    def test_is_inverted_trees_1tree_3node_false(self):
        """Провал проверки обратно ориентированного дерева из трех вершин."""
        self.graph.add_nodes_from(['a', 'b', 'c'])
        self.graph.add_edges_from([('a', 'c'), ('a', 'b')])
        self.assertFalse(GraphValidator.is_inverted_trees(self.graph))

    def test_get_tree_count_exception(self):
        """Провал проверки обратно ориентированного дерева из трех вершин."""
        self.graph.add_nodes_from(['a', 'b', 'c'])
        self.graph.add_edges_from([('a', 'c'), ('a', 'b')])
        self.assertFalse(GraphValidator.is_inverted_trees(self.graph))


    def test_is_inverted_trees_2tree_5node_has_loop(self):
        """Провал проверки обратно ориентированного дерева из трех вершин.
        Наличие цикла"""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e'])
        self.graph.add_edges_from([('c', 'b'), ('b', 'a'), ('a', 'c'),
                                   ('e', 'd')])
        self.assertFalse(GraphValidator.is_inverted_trees(self.graph))
        with self.assertRaises(ValueError) as error:
            GraphValidator.get_tree_count(self.graph)
        self.assertEqual(ERR_GRAPH_IS_NOT_INV_TREE, str(error.exception))

    def test_is_inverted_trees_3tree_13node_false(self):
        """Провал проверки леса обратно ориентированных деревьев."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                                   'j', 'k', 'l', 'm'])
        self.graph.add_edges_from([('d', 'a'), ('j', 'd'), ('e', 'b'),
                                   ('f', 'b'), ('k', 'e'), ('g', 'c'),
                                   ('h', 'c'), ('i', 'c'), ('l', 'g'),
                                   ('m', 'g'), ('l', 'n')])
        self.assertFalse(GraphValidator.is_inverted_trees(self.graph))

    def test_graph_has_loop_1tree_3node_true(self):
        """Наличие цикла в связном графе из трех вершин"""
        self.graph.add_nodes_from(['a', 'b', 'c'])
        self.graph.add_edges_from([('a', 'b'), ('b', 'c'), ('c', 'a')])
        self.assertTrue(GraphValidator.graph_has_loop(self.graph))

    def test_graph_has_loop_2tree_5node_true(self):
        """Наличие цикла в графе из пяти вершин и двух компонентов связности."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e'])
        self.graph.add_edges_from([('c', 'b'), ('b', 'a'), ('a', 'c'),
                                   ('e', 'd')])
        self.assertTrue(GraphValidator.graph_has_loop(self.graph))

    def test_graph_has_loop_3tree_13node_true(self):
        """Наличие цикла в графе из тринадцати вершин и трех компонентов
        связности."""
        self.graph.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                                   'j', 'k', 'l', 'm'])
        self.graph.add_edges_from([('d', 'a'), ('j', 'd'), ('e', 'b'),
                                   ('f', 'b'), ('k', 'e'), ('g', 'c'),
                                   ('h', 'c'), ('i', 'c'), ('l', 'g'),
                                   ('m', 'g'), ('l', 'n'), ('c', 'l')])
        self.assertTrue(GraphValidator.graph_has_loop(self.graph))


if __name__ == '__main__':
    unittest.main()
