import pytest
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    """Фикстура для генерации тестового списка транзакций."""
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


def test_filter_by_currency_usd(sample_transactions):
    generator = filter_by_currency(sample_transactions, "USD")
    result = list(generator)
    assert len(result) == 2
    assert result[0]["id"] == 93854
    assert result[1]["id"] == 14226


def test_filter_by_currency_missing(sample_transactions):
    generator = filter_by_currency(sample_transactions, "EUR")
    assert list(generator) == []


def test_filter_by_currency_empty():
    generator = filter_by_currency([], "USD")
    assert list(generator) == []


def test_filter_by_currency_corrupted_data():
    corrupted_transactions = [
        {"id": 111, "operationAmount": {}},
        {"id": 222, "operationAmount": {"currency": {"name": "USD", "code": "USD"}}},
    ]
    generator = filter_by_currency(corrupted_transactions, "USD")
    result = list(generator)
    assert len(result) == 1
    assert result[0]["id"] == 222


def test_transaction_descriptions_correct(sample_transactions):
    descriptions_gen = transaction_descriptions(sample_transactions)
    assert next(descriptions_gen) == "Перевод организации"
    assert next(descriptions_gen) == "Перевод со счета на счет"
    assert next(descriptions_gen) == "Оплата услуг"


def test_transaction_descriptions_empty():
    descriptions_gen = transaction_descriptions([])
    assert list(descriptions_gen) == []


def test_transaction_descriptions_missing_key():
    bad_transactions = [{"id": 123}]
    descriptions_gen = transaction_descriptions(bad_transactions)
    assert next(descriptions_gen) == "Описание отсутствует"


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator_variants(start, stop, expected):
    assert list(card_number_generator(start, stop)) == expected


def test_card_number_generator_stop_iteration():
    cards_gen = card_number_generator(1, 1)
    next(cards_gen)
    with pytest.raises(StopIteration):
        next(cards_gen)
