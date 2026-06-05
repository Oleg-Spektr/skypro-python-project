from unittest.mock import MagicMock, patch

import pytest

from src.external_api import convert_to_rub


@pytest.fixture
def usd_transaction() -> dict:
    """Фикстура тестовой транзакции в USD."""
    return {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}


def test_convert_to_rub_already_rub() -> None:
    """Тест: если валюта операции уже RUB, конвертация не требуется."""
    rub_transaction = {"operationAmount": {"amount": "150.50", "currency": {"code": "RUB"}}}
    assert convert_to_rub(rub_transaction) == 150.50


@patch("requests.get")
def test_convert_to_rub_success(mock_get: MagicMock, usd_transaction: dict) -> None:
    """Тест успешного обращения к внешнему API и конвертации."""
    # Имитируем успешный сетевой ответ от сервера со статусом 200
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 7500.0}
    mock_get.return_value = mock_response

    result = convert_to_rub(usd_transaction)
    assert result == 7500.0
    mock_get.assert_called_once()  # Проверяем, что запрос действительно отправлялся


@patch("requests.get")
def test_convert_to_rub_api_error(mock_get: MagicMock, usd_transaction: dict) -> None:
    """Тест: если внешний сервер вернул ошибку, возвращается 0.0."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    result = convert_to_rub(usd_transaction)
    assert result == 0.0


@patch("requests.get")
def test_convert_to_rub_invalid_data(mock_get: MagicMock) -> None:
    """Тест: если структура транзакции битая, возвращается 0.0."""
    corrupted_transaction = {"operationAmount": {}}
    result = convert_to_rub(corrupted_transaction)
    assert result == 0.0
    mock_get.assert_not_called()  # Запрос в сеть даже не должен отправляться
