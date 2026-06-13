import json
from unittest.mock import mock_open, patch

import pytest

from src.utils import get_financial_transactions, process_bank_operations, process_bank_search


def test_get_financial_transactions_success() -> None:
    """Тест успешного чтения корректного JSON-файла."""
    mock_data = [{"id": 1, "description": "Перевод"}]
    mock_json = json.dumps(mock_data)

    # Имитируем, что файл существует и возвращает наш JSON
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data=mock_json)):
        result = get_financial_transactions("fake_path.json")
        assert result == mock_data


def test_get_financial_transactions_file_not_found() -> None:
    """Тест: если файла нет на диске, должен вернуться пустой список."""
    with patch("os.path.exists", return_value=False):
        result = get_financial_transactions("missing.json")
        assert result == []


def test_get_financial_transactions_invalid_json() -> None:
    """Тест: если JSON сломан или пуст, должен вернуться пустой список."""
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data="invalid json")):
        result = get_financial_transactions("bad.json")
        assert result == []


def test_get_financial_transactions_not_a_list() -> None:
    """Тест: если в JSON лежит словарь вместо списка, возвращается пустой список."""
    mock_dict = {"id": 1}
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data=json.dumps(mock_dict))),
    ):
        result = get_financial_transactions("not_list.json")
        assert result == []


@pytest.fixture
def sample_data():
    return [
        {"id": 1, "description": "Перевод организации", "amount": "100.00"},
        {"id": 2, "description": "Открытие вклада", "amount": "5000.00"},
        {"id": 3, "description": "Перевод со счета на счет", "amount": "1200.00"},
        {"id": 4, "amount": "50.00"},  # Операция без описания
    ]


def test_process_bank_search_found(sample_data):
    """Тест успешного поиска операций (регистронезависимый)"""
    result = process_bank_search(sample_data, "перевод")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_process_bank_search_empty_query(sample_data):
    """Тест с пустой строкой поиска (должен вернуть все данные)"""
    result = process_bank_search(sample_data, "")
    assert len(result) == 4


def test_process_bank_search_no_match(sample_data):
    """Тест ситуации, когда совпадений не найдено"""
    result = process_bank_search(sample_data, "Ремонт")
    assert len(result) == 0


def test_process_bank_operations(sample_data):
    categories = ["Перевод", "Вклад", "Автокредит"]
    result = process_bank_operations(sample_data, categories)

    assert result["Перевод"] == 2
    assert result["Вклад"] == 1
    assert result["Автокредит"] == 0
