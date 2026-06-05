import json
from unittest.mock import mock_open, patch

from src.utils import get_financial_transactions


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
