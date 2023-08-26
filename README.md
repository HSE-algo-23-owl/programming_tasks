# Задания по программированию для курса "Алгоритмы и структуры данных" 💻

Задания предполагают реализацию на языке Python 3. Для выполнения заданий рекомендуется использовать 
[IDE PyCharm](https://www.jetbrains.com/pycharm/) в community версии, либо PyCharm Professional доступную по студенческой 
[лицензии](https://www.jetbrains.com/community/education/#students) (подтверждение статуса студента возможно через [GitHub Student Developer Pack](https://education.github.com/pack)). 

PyCharm имеет [встроенную интеграцию с Github](https://www.jetbrains.com/help/pycharm/github.html). После установки IDE PyCharm, необходимо добавить в IDE данные GitHub-аккаунта и клонировать репозиторий с заданиями.

Задания размещены в отдельных ветках репозитория, название которых начинается с префикса main, например ветка main_task_0.

**Для выполнения конкретного задания необходимо создать отдельную ветку** на основе ветки с заданием, назвать новую ветку в соответствии с веткой задания, заменив префикс main на название команды, например first_team_task_0.

В файле README.md в ветке задания расположена информация необходимая для его выполнения.

Как правило, для выполнения задания необходимо реализовать предложенные функции в файле main.py. В файлах с префиксом test расположены модульные тесты для проверки правильности реализации функций. Если необходимо реализовать несколько функций, например fibonacci и determinant, то в ветке будут соответствующие файлы с модульными тестами test_fibonacci.py и test_determinant.py, а также файл test_runner.py, объединяющий тесты из отдельных файлов. Провести тестирование можно путем запуска на выполнение файлов с модульными тестами или файла test_runner.py. Для проверки синтаксиса и оформления кода на Python рекомендуется пользоваться модулем flake8, т.к. данный модуль используется для автоматической проверки кода в репозитории.

После реализации предложенных функций, прохождения всех модульных тестов, проверки синтаксиса и оформления кода, необходимо зафиксировать изменения (git commit) и отправить их в репозиторий на Github (git push). После чего создать на Github запрос слияния с главной веткой задания (pull request). Важно не ошибиться с выбором веток для запроса, в base необходимо указать главную ветку, например main_task_0, а в compare указать собственную ветку с выполненным заданием, например first_team_task_1. В заголовке запроса можно указать название своей ветки, для удобного просмотра списка запросов на слияние. В описании запроса можно указать роли участников команды, выполнявших задание.

После создания запроса на слияние производится автоматический запуск тестов, ход выполнения и результаты можно посмотреть на вкладке Checks. Если выполнение тестов выявило ошибки, следует исправить их, снова зафиксировать и отправить изменения на Github, изменения автоматически отражаются в запросе на слияние. На вкладке Files changed видны изменения в файлах, по сравнению с целевой веткой. На вкладке Conversation ведется обсуждение выполненного задания. Если автоматическое тестирование не выявило ошибок, владелец репозитория проведет ревью кода и подтвердит его либо оставит вопросы или замечания. После подтверждения выполненное задание будет оценено и запрос на слияние будет закрыт.
