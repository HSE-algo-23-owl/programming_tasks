import random
import random as rnd
import string

import networkx as nx
import matplotlib.pyplot as plt
from bokeh.palettes import Spectral

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

        def generate_unique_name(length=3):
            return ''.join(random.choices(string.ascii_lowercase, k=length))

        def calculate_name_length(total_nodes):
            return max(1, len(str(total_nodes)))  # Минимальная длина, чтобы вместить уникальные имена

        def generate_uq_name(names):
            name = generate_unique_name()
            while name in names:
                name = generate_unique_name()
            return name

        forest = nx.DiGraph()

        # Множество для проверки уникальности имен
        unique_names = set()

        # Генерация деревьев
        for tree_index in range(tree_count):
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            root = generate_uq_name(unique_names)
            unique_names.add(root)
            forest.add_node(root, color=color, pos=(0, -tree_index))
            last_node = root

            for i in range(1, vertex_count):
                cur_node = generate_uq_name(unique_names)
                unique_names.add(cur_node)
                forest.add_node(cur_node, color=color, pos=(i, -tree_index))
                forest.add_edge(cur_node, last_node)

                if random.randint(0, 3) == 2:
                    last_node = cur_node

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
