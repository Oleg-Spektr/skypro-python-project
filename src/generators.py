from typing import Any, Dict, Generator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Generator[Dict[str, Any], None, None]:
    """Фильтрует транзакции по заданной валюте.

    Возвращает итератор, который поочередно выдает подходящие транзакции.
    """
    for transaction in transactions:
        try:
            if transaction["operationAmount"]["currency"]["code"] == currency:
                yield transaction
        except Exception:
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """Генерирует описание (description) для каждой транзакции поочередно.

    Если описание отсутствует, возвращает строку-заглушку.
    """
    for transaction in transactions:
        yield str(transaction.get("description", "Описание отсутствует"))


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Генерирует номера банковских карт в формате 'XXXX XXXX XXXX XXXX' в заданном диапазоне.

    Принимает стартовое и конечное числовое значение диапазона.
    """
    for number in range(start, stop + 1):
        str_num = f"{number:016d}"
        formatted_card = f"{str_num[:4]} {str_num[4:8]} {str_num[8:12]} {str_num[12:]}"
        yield formatted_card
