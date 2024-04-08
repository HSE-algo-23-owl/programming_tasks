# Задание №17
# Турнирный отбор
## Задачи  
1. В файле tournament.py реализовать функцию *tournament*, принимающую набор объектов для проведения турнира и функцию для выбора победителя турнира из двух объектов, и возвращающую объект победитель серии турниров, проведенных между переданными объектами.
## Примечания 
- Функция tournament принимает список или кортеж объектов (sample) и функцию get_winner, которая определяет победителя между двумя объектами. Затем проводится серия "турниров" между парами особей, и победители каждого турнира переходят на следующий этап, пока не останется один победитель.
- Функция tournament может принимать объекты любого типа, совместно с функцией, которая позволяет выбрать победителя из двух объектов соответствующего типа.
- Обратить внимание, что некоторые тесты ожидают вызов определенного вида исключения с заданным сообщением об ошибке.
- Разработку вести в отдельной ветке, созданной на основе данной. В названии ветки префикс main заменить на название команды.
- Корректность работы функции *tournament* проверить запустив файл test_tournament.py с модульными тестами.

## Пример турнирного отбора для выборки из трех объектов:
- **Шаг 1**: Изначально имеется три особи: A, B и C. Начинается с выбора двух особей для первого турнира. Предположим, выбраны A и B.
- **Шаг 2**: Сравниваются A и B с помощью функции get_winner, которая определяет, какая особь лучше. Предположим, A выигрывает, поэтому A переходит на следующий этап.
- **Шаг 3**: Теперь осталась одна особь, C, которую сравнивают с победителем предыдущего турнира, A.
- **Шаг 4**: Снова используется функция get_winner для сравнения A и C. Предположим, в этот раз C выигрывает.
- **Шаг 5**: Итоговый победитель, C возвращается как результат.
