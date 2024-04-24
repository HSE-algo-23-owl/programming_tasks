import random as rnd
import networkx as nx
import matplotlib.pyplot as plt


from graph_pack.constants import CHARS, ERR_NOT_INT_TREE_CNT, \
    ERR_LESS_THAN_1_TREE_CNT, ERR_NOT_INT_VERTEX_CNT, \
    ERR_LESS_THAN_1_VERTEX_CNT, ERR_VERTEX_CNT_LESS_THAN_TREE_CNT


class SimpleGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node, color=None):
        self.nodes[node] = {'color': color}
        self.edges[node] = []

    def add_edge(self, from_node, to_node):
        if from_node in self.edges:
            self.edges[from_node].append(to_node)


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

    def validate_input(tree_count: int, vertex_count: int):
        if not isinstance(tree_count, int):
            raise TypeError(ERR_NOT_INT_TREE_CNT)
        if tree_count < 1:
            raise ValueError(ERR_LESS_THAN_1_TREE_CNT)
        if not isinstance(vertex_count, int):
            raise TypeError(ERR_NOT_INT_VERTEX_CNT)
        if vertex_count < 1:
            raise ValueError(ERR_LESS_THAN_1_VERTEX_CNT)
        if vertex_count < tree_count:
            raise ValueError(ERR_VERTEX_CNT_LESS_THAN_TREE_CNT)

    @staticmethod
    def get_names(vertex_count: int) -> list:
        names = []
        for i in range(vertex_count):
            quotient = i + 1
            name = ''
            while quotient > 0:
                remainder = quotient % 26
                if remainder == 0:
                    name = 'z' + name
                    quotient = (quotient // 26) - 1
                else:
                    name = CHARS[remainder - 1] + name
                    quotient = quotient // 26
            names.append(name)
        return names

    @staticmethod
    def get_colours(tree_count: int) -> list:
        return ['#{:06x}'.format(rnd.randint(0, 0xFFFFFF)) for _ in range(tree_count)]

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
        GraphGenerator.validate_input(tree_count, vertex_count)

        graph = SimpleGraph()
        vertex_names = GraphGenerator.get_names(vertex_count)
        vertex_colours = GraphGenerator.get_colours(tree_count)

        for vertex, colour in zip(vertex_names, vertex_colours):
            graph.add_node(vertex, colour)

        for vertex in vertex_names[tree_count:]:
            graph.add_node(vertex)

        previous_vertex = vertex_names[:tree_count]
        left_border = tree_count
        right_border = tree_count + 1 if vertex_count > tree_count else vertex_count

        while left_border < vertex_count:
            present_vertex = vertex_names[left_border:right_border]
            for vertex in present_vertex:
                target_vertex = rnd.choice(previous_vertex)
                graph.add_edge(target_vertex, vertex)
                graph.nodes[vertex]['color'] = graph.nodes[target_vertex]['color']

            previous_vertex = present_vertex
            left_border = right_border
            right_border = rnd.randint(left_border + 1, vertex_count) if right_border < vertex_count else vertex_count

        return graph

    @staticmethod
    def show_plot(graph: nx.Graph) -> None:
        """Выводит изображение графа."""
        color_map = [graph.nodes[name]['color'] for name in graph.nodes]
        nx.draw_planar(graph, with_labels=True, node_color=color_map)
        plt.show()


if __name__ == '__main__':
    graph = GraphGenerator.generate_random_forest(3, 15)
    GraphGenerator.show_plot(graph)
