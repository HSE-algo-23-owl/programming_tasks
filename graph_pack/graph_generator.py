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

        if not isinstance(tree_count, int):
            raise TypeError("Expected integer for tree_count")
        if tree_count < 1:
            raise ValueError("tree_count must be greater than zero")

        if not isinstance(vertex_count, int):
            raise TypeError("Expected integer for vertex_count")
        if vertex_count < 1:
            raise ValueError("vertex_count must be greater than zero")
        if vertex_count < tree_count:
            raise ValueError("vertex_count cannot be less than tree_count")

        vertex_labels = GraphGenerator.generate_vertex_labels(vertex_count)
        vertex_colors = GraphGenerator.fetch_colors(tree_count)

        di_graph = nx.DiGraph()
        di_graph.add_nodes_from(vertex_labels)
        initial_vertices = vertex_labels[:tree_count]
        for node, color in zip(initial_vertices, vertex_colors):
            di_graph.nodes[node]['color'] = color

        if vertex_count == tree_count:
            start = tree_count
            end = vertex_count
        else:
            start = tree_count
            end = rnd.randint(tree_count + 1, vertex_count)

        current_vertices = []
        while start <= vertex_count:
            current_vertices = vertex_labels[start:end]
            if not current_vertices:
                break
            for current_vertex in current_vertices:
                chosen_vertex = rnd.choice(initial_vertices)
                di_graph.add_edge(current_vertex, chosen_vertex)
                di_graph.nodes[current_vertex]['color'] = di_graph.nodes[chosen_vertex]['color']
            initial_vertices = current_vertices
            start = end
            end = rnd.randint(start, vertex_count)
            if start == end and end != vertex_count:
                end += 1

        return di_graph

    def generate_vertex_labels(count: int) -> list:
        labels = []
        for index in range(count):
            number = index + 1
            label = ''
            while number > 0:
                mod = number % 26
                if mod == 0:
                    label = 'z' + label
                    number = (number // 26) - 1
                else:
                    label = 'abcdefghijklmnopqrstuvwxyz'[mod - 1] + label
                    number //= 26
            labels.append(label)
        return labels

    def fetch_colors(number_of_trees: int) -> list:
        color_list = []
        for _ in range(number_of_trees):
            random_color = '#{:06x}'.format(rnd.randint(0, 0xFFFFFF))
            color_list.append(random_color)
        return color_list

    @staticmethod
    def show_plot(graph: nx.Graph) -> None:
        """Выводит изображение графа."""
        color_map = [graph.nodes[name]['color'] for name in graph.nodes]
        nx.draw_planar(graph, with_labels=True, node_color=color_map)
        plt.show()


if __name__ == '__main__':
    graph = GraphGenerator.generate_random_forest(3, 15)
    GraphGenerator.show_plot(graph)
