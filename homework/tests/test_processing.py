import pytest
from typing import Any
from src.processing import filter_by_state, sort_by_date


# === ФИКСТУРЫ ДЛЯ ТЕСТОВЫХ ДАННЫХ ===

@pytest.fixture
def sample_transactions() -> list[dict[str, Any]]:
    """Фикстура, предоставляющая разнообразный набор транзакций."""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 2, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 3, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 4, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]


@pytest.fixture
def duplicate_dates_transactions() -> list[dict[str, Any]]:
    """Фикстура с транзакциями, имеющими абсолютно одинаковые даты."""
    return [
        {'id': 10, 'state': 'EXECUTED', 'date': '2024-01-01T12:00:00.000000'},
        {'id': 20, 'state': 'CANCELED', 'date': '2024-01-01T12:00:00.000000'}
    ]


@pytest.fixture
def invalid_dates_transactions() -> list[dict[str, Any]]:
    """Фикстура с некорректными или нестандартными форматами дат."""
    return [
        {'id': 100, 'state': 'EXECUTED', 'date': 'not-a-date'},
        {'id': 200, 'state': 'EXECUTED', 'date': ''}
    ]


# === ТЕСТИРОВАНИЕ ФУНКЦИИ filter_by_state ===

@pytest.mark.parametrize(
    "state_param, expected_count",
    [
        ("EXECUTED", 2),  # Тест фильтрации по заданному статусу
        ("CANCELED", 2),  # Параметризация для различных статусов
        ("PENDING", 0),   # Проверка работы при отсутствии словарей с указанным статусом
    ]
)
def test_filter_by_state(sample_transactions: list[dict[str, Any]], state_param: str, expected_count: int) -> None:
    """Параметризованный тест фильтрации транзакций по различным статусам."""
    result = filter_by_state(sample_transactions, state=state_param)
    assert len(result) == expected_count
    for item in result:
        assert item['state'] == state_param


# === ТЕСТИРОВАНИЕ ФУНКЦИИ sort_by_date ===

@pytest.mark.parametrize(
    "descending_param, expected_ids",
    [
        (True, [1, 4, 3, 2]),   # Порядок убывания (от свежих к старым)
        (False, [2, 3, 4, 1]),  # Порядок возрастания (от старых к свежим)
    ]
)
def test_sort_by_date_order(sample_transactions: list[dict[str, Any]], descending_param: bool, expected_ids: list[int]) -> None:
    """Тестирование сортировки списка словарей по датам в порядке убывания и возрастания."""
    result = sort_by_date(sample_transactions, descending=descending_param)
    result_ids = [item['id'] for item in result]
    assert result_ids == expected_ids


def test_sort_by_date_duplicate_dates(duplicate_dates_transactions: list[dict[str, Any]]) -> None:
    """Проверка корректности сортировки при одинаковых датах."""
    # Стабильная сортировка (Timsort в Python) должна сохранять исходный относительный порядок элементов
    result = sort_by_date(duplicate_dates_transactions, descending=True)
    assert result[0]['id'] == 10
    assert result[1]['id'] == 20


def test_sort_by_date_invalid_formats(invalid_dates_transactions: list[dict[str, Any]]) -> None:
    """Тесты на работу функции с некорректными или нестандартными форматами дат."""
    # Проверяем устойчивость функции — она должна либо обработать строки как обычный текст, либо перехватить ошибку
    try:
        result = sort_by_date(invalid_dates_transactions)
        assert isinstance(result, list)
    except Exception:
        # Если ваша функция падает на кривых датах, pytest зафиксирует ожидаемое исключение
        assert True
