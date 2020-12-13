# Джанго приложение с интерфейсом и реализацией некоторых алгоритмов нахождения редуктов

- основной код логики находится в `reducts/logic.py`
- пример данных в `reducts/examples.py`

# Установка

## Вариант №1 (без Pipenv)

1. Создать окружение
    ```
    python -m venv venv
    ```
2. Активировать окружение
    ```
    ## Linux
    source venv/bin/activate
    ## Windows CMD.exe
    .\venv\scripts\activate.bat
    ## Windows PowerShell
    .\venv\scripts\Activate.ps1
    ```
3. Установка зависимостей
    ```
    pip install -r requirements
    ```
4. Запуск
    ```
    python manage.py runserver
    ```

## Вариант №2 (с Pipenv)

1. `pipenv install`
2. `pipenv run ./manage.py runserver`