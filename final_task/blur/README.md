# Алгоритм обхода графа в ширину
## Описание алгоритма
Алгоритм обхода графа в ширину используется для поиска в графах и деревьях (англ. breadth-first search, BFS). Этот алгоритм начинает с 
корневого узла и исследует все узлы на текущем уровне перед переходом к узлам на следующем уровне. Для реализации данного алгоритма обычно используется очередь.

## Шаги алгоритма
### Инициализация 
Начнем с какого-то начального узла (стартового узла). Добавим его в очередь и отметим как посещенный.

### Обработка, пока очередь не пуста
Извлечем узел из очереди.
Обработаем этот узел (например, выведем его или запомним его значение).
Добавим в очередь все непосещенные соседние узлы текущего узла и отметим их как посещенные.

### Повторение 
Продолжаем процесс, пока очередь не станет пустой.

## Входные/выходные данные:
### Входные данные:
1. Граф, представленный в виде списка смежности, где каждой вершине соответствует список связанных с ней вершин.   
2. Вершина, с которой начинается обход, представлена в виде строки, содержащей в себе наименование вершины, содержащейся в графе.

### Выходные данные:
Порядок обхода вершин графа представлен в виде списка.

## Области допустимых значений:
### Входные данные
Начальная вершина должна принадлежать множеству вершин графа.
### Выходные данные
Последовательность вершин содержит все вершины графа, которые достижимы из начальной вершины.

## Пример выполнения алгоритма BFS

Рассмотрим граф, представленный в виде списка смежности:

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    B-->E;
    C-->F;
```
### Смежные вершины:
A: [B, C]  
B: [A, D, E]  
C: [A, F]  
D: [B]  
E: [B]  
F: [C]

## Шаги выполнения алгоритма

### Инициализация

Начальный узел: A  
Очередь: A  
Посещенные узлы: A  

### Первый цикл
Очередь: пустая  
Извлеченный узел: A  
Обработка: A  
Соседи A: B, C  
Очередь: B, C  
Посещенные узлы: A, B, C

### Второй цикл
Очередь: C  
Извлеченный узел: B  
Обработка: B  
Соседи B: A, D, E (A уже посещен)  
Очередь: C, D, E  
Посещенные узлы: A, B, C, D, E  

### Третий цикл
Очередь: D, E  
Извлеченный узел: C  
Обработка: C  
Соседи C: A, F (A уже посещен)  
Очередь: D, E, F  
Посещенные узлы: A, B, C, D, E, F  

### Четвертый цикл
Очередь: E, F  
Извлеченный узел: D  
Обработка: D  
Соседи D: B (B уже посещен)  
Очередь: E, F  
Посещенные узлы: A, B, C, D, E, F

### Пятый цикл
Очередь: F  
Извлеченный узел: E  
Обработка: E  
Соседи E: B (B уже посещен)  
Очередь: F  
Посещенные узлы: A, B, C, D, E, F

### Шестой цикл
Очередь: пустая  
Извлеченный узел: F  
Обработка: F  
Соседи F: C (C уже посещен)  
Очередь: пустая  
Посещенные узлы: A, B, C, D, E, F  

## Итог
Очередь пуста, алгоритм завершен. Все узлы графа посещены в порядке: A, B, C, D, E, F.
