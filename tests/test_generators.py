import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 93854,
            "state": "EXECUTED",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 14225,
            "state": "EXECUTED",
            "operationAmount": {"amount": "142.00", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 14226,
            "state": "EXECUTED",
            "operationAmount": {"amount": "500.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Оплата услуг",
        },
    ]


# ==================== 1) ТЕСТЫ FILTER_BY_CURRENCY ====================


def test_filter_by_currency_usd(sample_transactions):
    """Проверка корректной фильтрации транзакций по заданной валюте."""
    generator = filter_by_currency(sample_transactions, "USD")
    result = list(generator)
    assert len(result) == 2
    assert result[0]["id"] == 93854
    assert result[1]["id"] == 14226


def test_filter_by_currency_missing(sample_transactions):
    """Проверка случая, когда транзакции в заданной валюте отсутствуют."""
    generator = filter_by_currency(sample_transactions, "EUR")
    assert list(generator) == []


def test_filter_by_currency_empty():
    """Проверка, что генератор не падает на пустом списке."""
    generator = filter_by_currency([], "USD")
    assert list(generator) == []


def test_filter_by_currency_corrupted_data():
    """Проверка, что генератор пропускает транзакции с битой структурой."""
    corrupted_transactions = [
        {"id": 111, "operationAmount": {}},  # Нет ключа currency
        {"id": 222, "operationAmount": {"currency": {"name": "USD", "code": "USD"}}},  # Хорошая транзакция
    ]
    generator = filter_by_currency(corrupted_transactions, "USD")
    result = list(generator)

    assert len(result) == 1
    assert result[0]["id"] == 222


# ==================== 2) ТЕСТЫ TRANSACTION_DESCRIPTIONS ====================


def test_transaction_descriptions_correct(sample_transactions):
    """Проверка возврата корректных описаний для каждой транзакции."""
    descriptions_gen = transaction_descriptions(sample_transactions)
    assert next(descriptions_gen) == "Перевод организации"
    assert next(descriptions_gen) == "Перевод со счета на счет"
    assert next(descriptions_gen) == "Оплата услуг"


def test_transaction_descriptions_empty():
    """Тестирование работы функции с пустым списком транзакций."""
    descriptions_gen = transaction_descriptions([])
    assert list(descriptions_gen) == []


def test_transaction_descriptions_missing_key():
    """Проверка работы, если ключ description отсутствует."""
    bad_transactions = [{"id": 123}]
    descriptions_gen = transaction_descriptions(bad_transactions)
    assert next(descriptions_gen) == "Описание отсутствует"


# ==================== 3) ТЕСТЫ CARD_NUMBER_GENERATOR ====================


def test_card_number_generator_range_and_formatting():
    """Проверка выдачи номеров в диапазоне и корректности форматирования."""
    cards_gen = card_number_generator(1, 2)
    assert next(cards_gen) == "0000 0000 0000 0001"
    assert next(cards_gen) == "0000 0000 0000 0002"


def test_card_number_generator_limits_and_stop():
    """Проверка крайних значений и корректного завершения генерации (StopIteration)."""
    cards_gen = card_number_generator(9999999999999999, 9999999999999999)
    assert next(cards_gen) == "9999 9999 9999 9999"

    # Проверяем, что генератор правильно завершил работу и больше ничего не выдает
    with pytest.raises(StopIteration):
        next(cards_gen)
