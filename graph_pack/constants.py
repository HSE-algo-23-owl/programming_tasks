"""В модуле представлены константы пакета для работы с графами."""

CHARS = 'abcdefghijklmnopqrstuvwxyz'
"""Символы для генерации названий вершин графа"""

ERR_NOT_INT_TREE_CNT = 'Количество деревьев не является целым числом'
"""Текст сообщения об ошибке для валидации входных данных класса 
GraphGenerator"""

ERR_LESS_THAN_1_TREE_CNT = 'Количество деревьев не может быть меньше 1'
"""Текст сообщения об ошибке для валидации входных данных класса 
GraphGenerator"""

ERR_NOT_INT_VERTEX_CNT = 'Количество вершин не является целым числом'
"""Текст сообщения об ошибке для валидации входных данных класса 
GraphGenerator"""

ERR_LESS_THAN_1_VERTEX_CNT = 'Количество вершин не может быть меньше 1'
"""Текст сообщения об ошибке для валидации входных данных класса 
GraphGenerator"""

ERR_VERTEX_CNT_LESS_THAN_TREE_CNT = ('Количество вершин не может быть меньше '
                                     'количества деревьев')
"""Текст сообщения об ошибке для валидации входных данных класса 
GraphGenerator"""

ERR_GRAPH_IS_NOT_INV_TREE = ('Граф является обратно ориентированным '
                             'деревом/лесом')
"""Текст сообщения об ошибке для валидации входных данных класса 
GraphValidator"""
