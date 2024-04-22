import random as rnd
import time

import networkx as nx
import matplotlib.pyplot as plt
from math import log2


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

        GraphGenerator.__validate_params(tree_count, vertex_count)

        colors = GraphGenerator.__get_colors(tree_count)
        names = GraphGenerator.__get_names(vertex_count)
        graph = nx.DiGraph()

        depth = 1
        leafs = [list(), []]  # список листьев по уровням
        existing_coordinates = []

        for i, color in enumerate(colors, start=1):  # генерация стоков
            node_name = names.pop(0)
            graph.add_node(node_name, color=color, pos=(i*5000, 0))
            leafs[0].append(node_name)

        while names:  # пока есть имена для узлов
            parent_name = rnd.choice(leafs[0])
            leafs[0].remove(parent_name)

            parent_node = graph.nodes[parent_name]

            cnt_child = rnd.randint(1, int(log2(len(names)) // tree_count + 1))  # расчет количества потомков

            x = parent_node["pos"][0] // (cnt_child * 2)  # расчет координаты расположения
            if parent_name in [chr(97 + i) for i in range(tree_count)]:
                x //= 4
            coordinates = []

            for i in range(1, cnt_child // 2 + 1):
                coordinates.append(parent_node["pos"][0] - x * i)

            for i in range(1, cnt_child // 2 + 1):
                coordinates.append(parent_node["pos"][0] + x * i)

            if cnt_child % 2 != 0:
                coordinates.append(parent_node["pos"][0])

            coordinates.sort()

            while cnt_child:
                child_name = names.pop(rnd.randint(0, len(names)-1))
                x_coord = coordinates.pop(0)
                while (x_coord, depth*100) in existing_coordinates:  # пока присутствуют совпадающие координаты
                    x_coord += 500
                graph.add_node(child_name, color=parent_node['color'], pos=(x_coord, depth*100))
                existing_coordinates.append((x_coord, depth*100))
                leafs[-1].append(child_name)
                graph.add_edge(child_name, parent_name)

                cnt_child -= 1

            if not leafs[0]:  # если на уровне не осталось узлов
                del leafs[0]  # удаляем уровень

                parent_count = rnd.randint(1, int(vertex_count / (tree_count * depth)) + 1)  # кол-во родителей на новом уровне

                if parent_count > len(leafs[0]):
                    parent_count = len(leafs[0])

                if parent_count > 0:
                    random_leafs = rnd.choices(leafs[0], k=parent_count)
                    leafs[0] = random_leafs

                leafs.append([])
                depth += 1

        return graph

    @staticmethod
    def show_plot(graph: nx.Graph) -> None:
        """Выводит изображение графа."""
        color_map = [graph.nodes[name]['color'] for name in graph.nodes]
        #nx.draw_planar(graph, with_labels=True, node_color=color_map)

        pos = {node: graph.nodes[node]['pos'] for node in graph.nodes}

        nx.draw(graph, pos, with_labels=True, node_color=color_map)

        plt.show()

    @staticmethod
    def __validate_params(tree_count, vertex_count) -> None:
        """Генерирует случайные цвета для покраски деревьев."""
        if type(tree_count) != int:
            raise TypeError(ERR_NOT_INT_TREE_CNT)

        if type(vertex_count) != int:
            raise TypeError(ERR_NOT_INT_VERTEX_CNT)

        if tree_count < 1:
            raise ValueError(ERR_LESS_THAN_1_TREE_CNT)

        if vertex_count < 1:
            raise ValueError(ERR_LESS_THAN_1_VERTEX_CNT)

        if vertex_count < tree_count:
            raise ValueError(ERR_VERTEX_CNT_LESS_THAN_TREE_CNT)

    @staticmethod
    def __get_colors(tree_count: int) -> list[str]:
        """Генерирует случайные цвета для покраски деревьев."""
        return ['#{:06x}'.format(rnd.randint(0, 0xFFFFFF)) for _ in range(tree_count)]

    @staticmethod
    def __get_names(vertex_count: int) -> list[str]:
        """Генерирует уникальные имена вершин деревьев."""
        names = []

        for i in range(1, vertex_count + 1):
            name = ""
            while i:
                i -= 1
                name += chr(97 + i % 26)
                i //= 26

            names.append(name[::-1])

        return names


if __name__ == '__main__':
    graph = GraphGenerator.generate_random_forest(3, 20)
    GraphGenerator.show_plot(graph)