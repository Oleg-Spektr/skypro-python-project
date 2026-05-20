from typing import Any, Dict, Generator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Generator[Dict[str, Any], None, None]:
    """
    Фильтрует транзакции по заданной валюте.
    Возвращает итератор, который поочередно выдает подходящие транзакции.
    """
    for transaction in transactions:
        # Проверяем безопасный доступ к вложенной структуре валюты
        try:
            current_currency = transaction["operationAmount"]["currency"]["code"]
            if current_currency == currency:
                yield transaction
        except KeyError:
            # Если ключи отсутствуют в структуре, пропускаем транзакцию
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Генерирует описание (description) для каждой транзакции поочередно.
    Если описание отсутствует, возвращает строку-заглушку.
    """
    for transaction in transactions:
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генерирует номера банковских карт в формате 'XXXX XXXX XXXX XXXX' в заданном диапазоне.
    Принимает стартовое и конечное числовое значение диапазона.
    """
    for number in range(start, end + 1):
        # Превращаем число в 16-значную строку с ведущими нулями
        str_num = f"{number:016d}"
        # Форматируем строку, разделяя по 4 цифры через пробел
        formatted_card = f"{str_num[:4]} {str_num[4:8]} {str_num[8:12]} {str_num[12:]}"
        yield formatted_card
