import re
from typing import Any, Dict, List, Optional, TypedDict


# Описываем строгие типы для внутренней структуры банковской операции
class CurrencyDict(TypedDict):
    name: str
    code: str


class OperationAmountDict(TypedDict):
    amount: str
    currency: CurrencyDict


class TransactionDict(TypedDict):
    date: str
    description: str
    operationAmount: OperationAmountDict


def main() -> None:
    """Основная логика приложения для работы с банковскими транзакциями."""
    # --- Шаг 1. Приветствие и выбор формата файла ---
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    user_choice: str = input("Пользователь: ").strip()
    print()

    if user_choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
    elif user_choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
    elif user_choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
    else:
        print("Программа: Некорректный выбор. Пожалуйста, запустите программу снова.")
        return

    # Явно указываем тип списка транзакций через TypedDict
    transactions: List[Dict[str, Any]] = [
        {
            "date": "2019-12-08T22:46:13.431412",
            "description": "Открытие вклада",
            "operationAmount": {
                "amount": "40542",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "from": None,
            "to": "Счет **4321",
        },
        {
            "date": "2019-11-12T10:11:12.123456",
            "description": "Перевод с карты на карту",
            "operationAmount": {
                "amount": "130",
                "currency": {"name": "USD", "code": "USD"},
            },
            "from": "MasterCard 7771 27** **** 3727",
            "to": "Visa Platinum 1293 38** **** 9203",
        },
        {
            "date": "2018-07-18T15:20:34.987654",
            "description": "Перевод организации",
            "operationAmount": {
                "amount": "8390",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "from": "Visa Platinum 7492 65** **** 7202",
            "to": "Счет **0034",
        },
        {
            "date": "2018-06-03T08:12:10.000001",
            "description": "Перевод со счета на счет",
            "operationAmount": {
                "amount": "8200",
                "currency": {"name": "EUR", "code": "EUR"},
            },
            "from": "Счет **2935",
            "to": "Счет **4321",
        },
    ]

    # --- Шаг 2. Фильтрация по статусу ---
    valid_statuses: List[str] = ["EXECUTED", "CANCELED", "PENDING"]
    print()

    while True:
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        raw_status: str = input("Пользователь: ").strip()
        user_status: str = raw_status.upper()

        if user_status in valid_statuses:
            print(f'Программа: Операции отфильтрованы по статусу "{user_status}"')
            break
        else:
            print(f'Программа: Статус операции "{raw_status}" недоступен.\n')

    # --- Шаг 3. Сортировка по дате ---
    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    sort_choice: str = input("Пользователь: ").strip().lower()

    if sort_choice == "да":
        print("Программа: Отсортировать по возрастанию или по убыванию?")
        sort_order: str = input("Пользователь: ").strip().lower()

        is_descending: bool = True
        if "возрастанию" in sort_order:
            is_descending = False

        transactions.sort(key=lambda x: str(x.get("date", "")), reverse=is_descending)

    # --- Шаг 4. Фильтрация по валюте (Рубли) ---
    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    rub_choice: str = input("Пользователь: ").strip().lower()

    if rub_choice == "да":
        transactions = [
            op
            for op in transactions
            if isinstance(op.get("operationAmount"), dict)
            and isinstance(op["operationAmount"].get("currency"), dict)
            and op["operationAmount"]["currency"].get("name") == "руб."
        ]

    # --- Шаг 5. Фильтрация по подстроке в описании ---
    print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    search_choice: str = input("Пользователь: ").strip().lower()

    if search_choice == "да":
        search_word: str = input("Пользователь: ").strip()
        if search_word:
            pattern: re.Pattern[str] = re.compile(re.escape(search_word), re.IGNORECASE)
            transactions = [
                op
                for op in transactions
                if isinstance(op.get("description"), str) and pattern.search(op["description"])
            ]

    # --- Шаг 6. Итоговый вывод результатов ---
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Программа:\nВсего банковских операций в выборке: {len(transactions)}")
    print()

    for op in transactions:
        raw_date: Any = op.get("date", "")
        formatted_date: str = ""
        if isinstance(raw_date, str) and len(raw_date) >= 10:
            year, month, day = raw_date[:10].split("-")
            formatted_date = f"{day}.{month}.{year}"

        description: str = str(op.get("description", ""))

        source: Optional[Any] = op.get("from")
        target: str = str(op.get("to", ""))

        transfer_route: str = f"{source} -> {target}" if source else target

        # Безопасное извлечение вложенных данных для mypy
        amount: str = ""
        currency: str = ""
        op_amount: Any = op.get("operationAmount")

        if isinstance(op_amount, dict):
            amount = str(op_amount.get("amount", ""))
            op_currency: Any = op_amount.get("currency")
            if isinstance(op_currency, dict):
                currency = str(op_currency.get("name", ""))

        print(f"{formatted_date} {description}")
        print(transfer_route)
        print(f"Сумма: {amount} {currency}")
        print()


if __name__ == "__main__":
    main()
