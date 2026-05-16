import pytest
from typing import Any
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_transactions() -> list[dict[str, Any]]:
    """Фикстура, предоставляющая базовый набор транзакций для тестов."""
    return [
        {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]


# Параметризуем тест фильтрации: проверяем разные статусы и ожидаемое количество результатов
@pytest.mark.parametrize(
    "state_param, expected_count",
    [
        ("EXECUTED", 2),
        ("CANCELED", 2),
        ("PENDING", 0),  # несуществующий статус должен возвращать пустой список
    ]
)
def test_filter_by_state(sample_transactions: list[dict[str, Any]], state_param: str, expected_count: int) -> None:
    """Тест фильтрации транзакций по различным статусам."""
    result = filter_by_state(sample_transactions, state=state_param)
    assert len(result) == expected_count
    for item in result:
        assert item['state'] == state_param


def test_filter_by_state_default(sample_transactions: list[dict[str, Any]]) -> None:
    """Тест фильтрации со статусом по умолчанию (EXECUTED)."""
    result = filter_by_state(sample_transactions)
    assert len(result) == 2
    for item in result:
        assert item['state'] == 'EXECUTED'


# Параметризуем тест сортировки: проверяем по убыванию (True) и по возрастанию (False)
@pytest.mark.parametrize(
    "descending_param, expected_first_id",
    [
        (True, 414288290),   # Самая свежая дата (2019 год) должна быть первой
        (False, 939719570),  # Самая старая дата (июнь 2018 года) должна быть первой
    ]
)
def test_sort_by_date(sample_transactions: list[dict[str, Any]], descending_param: bool, expected_first_id: int) -> None:
    """Тест сортировки транзакций по дате с разным порядком."""
    result = sort_by_date(sample_transactions, descending=descending_param)
    assert len(result) == len(sample_transactions)
    assert result[0]['id'] == expected_first_id
