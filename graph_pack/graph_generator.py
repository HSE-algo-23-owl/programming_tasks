import random as rnd
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

        # ERR_NOT_INT_TREE_CNT = "tree_count must be an integer"
        # ERR_LESS_THAN_1_TREE_CNT = "tree_count must be at least 1"
        # ERR_NOT_INT_VERTEX_CNT = "vertex_count must be an integer"
        # ERR_LESS_THAN_1_VERTEX_CNT = "vertex_count must be at least 1"
        # ERR_VERTEX_CNT_LESS_THAN_TREE_CNT = "vertex_count cannot be less than tree_count"

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

        vertex_name_list = []
        for i in range(vertex_count):
            num = i + 1
            vertex_name = ""
            while num > 0:
                r = num % 26
                if r == 0:
                    vertex_name = 'z' + vertex_name
                    num = (num // 26) - 1
                else:
                    vertex_name = 'abcdefghijklmnopqrstuvwxyz'[r - 1] + vertex_name
                    num //= 26
            vertex_name_list.append(vertex_name)

        vertex_colour_list = ['#{:06x}'.format(rnd.randint(0, 0xFFFFFF)) for _ in range(tree_count)]

        directed_graph = nx.DiGraph()
        directed_graph.add_nodes_from(vertex_name_list)
        previous_vertices = vertex_name_list[:tree_count]
        for vertex, colour in zip(previous_vertices, vertex_colour_list):
            directed_graph.nodes[vertex]['color'] = colour

        if vertex_count == tree_count:
            left = tree_count
            right = vertex_count
        else:
            left = tree_count
            right = rnd.randint(tree_count + 1, vertex_count)
        while left <= vertex_count:
            current_vertices = vertex_name_list[left:right]
            if not current_vertices:
                break
            for current_vertex in current_vertices:
                target = rnd.choice(previous_vertices)
                directed_graph.add_edge(current_vertex, target)
                directed_graph.nodes[current_vertex]['color'] = directed_graph.nodes[target]['color']
            previous_vertices = current_vertices
            left = right
            right = rnd.randint(left, vertex_count)
            if left == right and right != vertex_count:
                right += 1

        graph = directed_graph

    @staticmethod
    def show_plot(graph: nx.Graph) -> None:
        """Выводит изображение графа."""
        color_map = [graph.nodes[name]['color'] for name in graph.nodes]
        nx.draw_planar(graph, with_labels=True, node_color=color_map)
        plt.show()


if __name__ == '__main__':
    graph = GraphGenerator.generate_random_forest(3, 15)
    GraphGenerator.show_plot(graph)
