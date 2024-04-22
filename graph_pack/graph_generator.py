import random
import random as rnd
import string

import networkx as nx
import matplotlib.pyplot as plt


from graph_pack.constants import CHARS, ERR_NOT_INT_TREE_CNT, \
    ERR_LESS_THAN_1_TREE_CNT, ERR_NOT_INT_VERTEX_CNT, \
    ERR_LESS_THAN_1_VERTEX_CNT, ERR_VERTEX_CNT_LESS_THAN_TREE_CNT


class GraphGenerator:
    """Класс для генерации графа.

    Methods
    -------
    generate_random_forest(tree_count: int = 3, vertex_count: int = 15)\
            -> nx.Graph:
        Возвращает случайно сгенерированный граф, представляющий собой
        лес из обратно ориентированных деревьев.

    show_plot(graph: nx.Graph) -> None:
        Выводит изображение графа.
    """

    @staticmethod
    def generate_random_forest(tree_count: int = 3, vertex_count: int = 15)\
            -> nx.Graph:
        """Возвращает случайно сгенерированный граф, представляющий собой
        лес из обратно ориентированных деревьев. Названия вершин уникальны
        и состоят из латинских букв. Вершины, относящиеся к одному дереву,
        имеют одинаковый цвет.

        :param tree_count: Количество деревьев в графе.
        :param vertex_count:Количество вершин в графе.
        :raises TypeError: Если количество вершин или количество деревьев
        не являются целыми числами.
        :raises ValueError: Если количество вершин или количество деревьев
        меньше единицы, если количество вершин меньше чем количество деревьев.
        :return: Граф.
        """
       #validation
        if type(tree_count) != int:
            raise TypeError(ERR_NOT_INT_TREE_CNT)

        elif type(vertex_count) != int:
            raise TypeError(ERR_NOT_INT_VERTEX_CNT)

        elif tree_count < 1:
            raise ValueError(ERR_LESS_THAN_1_TREE_CNT)

        elif vertex_count < 1:
            raise ValueError( ERR_LESS_THAN_1_VERTEX_CNT)

        elif tree_count > vertex_count:
            raise ValueError(ERR_VERTEX_CNT_LESS_THAN_TREE_CNT)

        trees = []

        def generate_tree():
            tree = nx.DiGraph()
            vertices = [random.choice(string.ascii_uppercase) for _ in range(vertex_count)]
            tree.add_nodes_from(vertices)
            root = vertices[0]
            for v in vertices[1:]:
                parent = random.choice(vertices[:vertices.index(v)])
                tree.add_edge(parent, v)
            return tree

        # Generate trees
        for _ in range(tree_count):
            tree = generate_tree()
            trees.append(tree)

        forest = nx.DiGraph()
        for i, tree in enumerate(trees):
            forest = nx.compose(forest, tree)

        # Assign colors to nodes in the same tree
        colors = {}
        for i, tree in enumerate(trees):
            color = plt.cm.get_cmap('tab20', tree_count)(i % 20)  # To limit colors to 20 distinct colors
            for node in tree.nodes():
                colors[node] = color

        plt.figure()
        pos = nx.spring_layout(forest)
        nx.draw(forest, pos, with_labels=True, node_color=[colors.get(node) for node in forest.nodes()],
                cmap=plt.get_cmap('tab20'), node_size=1000)
        plt.show()

        return forest


    @staticmethod
    def show_plot(graph: nx.Graph) -> None:
        """Выводит изображение графа."""
        color_map = [graph.nodes[name]['color'] for name in graph.nodes]
        nx.draw_planar(graph, with_labels=True, node_color=color_map)
        plt.show()


if __name__ == '__main__':
    graph = GraphGenerator.generate_random_forest(3, 15)
    GraphGenerator.show_plot(graph)
