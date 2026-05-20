## Тестирование

В проекте реализовано модульное тестирование с использованием фреймворка `pytest`. Написаны параметризованные тесты и применены фикстуры для проверки корректности работы функций, граничных случаев и обработки некорректных входных данных.

### Запуск тестов и проверка покрытия:
Для запуска тестов с выводом отчета о покрытии кода в терминал выполните команду:
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

### Генерация HTML-отчета:
Для создания подробного визуального отчета о покрытии в формате HTML выполните:
```bash
python -m pytest tests/ --cov=. --cov-report=html
```
Отчет генерируется в папку `htmlcov/`. Чтобы посмотреть его, откройте файл `htmlcov/index.html` в любом браузере.



## Модуль `generators` (Работа с большими объемами данных)

Модуль предназначен для эффективной потоковой обработки массивов транзакций с помощью функций-генераторов. Использование генераторов (`yield`) позволяет минимизировать потребление оперативной памяти, так как элементы обрабатываются поочередно.

### Примеры использования на официальных данных

```python
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

# Входные данные для проверки
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952", "to": "Счет 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542", "to": "Счет 75651667383060284188"
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719", "to": "Счет 74489636417521191160"
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658", "to": "Visa Platinum 8990922113665229"
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588", "to": "Счет 14211924144426031657"
    }
]

# 1. Фильтрация по USD
usd_transactions = filter_by_currency(transactions, "USD")
print(len(list(usd_transactions)))  # Выведет: 3

# 2. Получение описаний операций
descriptions = transaction_descriptions(transactions)
print(next(descriptions))  # Выведет: "Перевод организации"

# 3. Генерация номеров карт в диапазоне
cards = card_number_generator(1, 2)
print(next(cards))  # Выведет: "0000 0000 0000 0001"
```
