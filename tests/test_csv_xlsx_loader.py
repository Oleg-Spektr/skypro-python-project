from unittest.mock import patch

import pandas as pd

from src.csv_xlsx_loader import load_transactions_from_csv, load_transactions_from_xlsx

# --- Тесты для функции load_transactions_from_csv ---

@patch("src.csv_xlsx_loader.os.path.exists")
@patch("src.csv_xlsx_loader.pd.read_csv")
def test_load_csv_success(mock_read_csv, mock_exists):
    """Тест успешного чтения CSV с использованием patch."""
    mock_exists.return_value = True

    # Создаем фейковый DataFrame для возврата
    fake_df = pd.DataFrame([
        {"id": 1, "state": "EXECUTED", "description": "Перевод"},
        {"id": 2, "state": "CANCELED", "description": None}
    ])
    mock_read_csv.return_value = fake_df

    result = load_transactions_from_csv("dummy_path.csv")

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["description"] is None
    mock_read_csv.assert_called_once_with("dummy_path.csv", sep=";")


@patch("src.csv_xlsx_loader.os.path.exists")
def test_load_csv_file_not_found(mock_exists):
    """Тест ситуации, когда CSV-файл отсутствует на диске."""
    mock_exists.return_value = False
    result = load_transactions_from_csv("non_existent.csv")
    assert result == []


# --- Тесты для функции load_transactions_from_xlsx ---

@patch("src.csv_xlsx_loader.os.path.exists")
@patch("src.csv_xlsx_loader.pd.read_excel")
def test_load_xlsx_success(mock_read_excel, mock_exists):
    """Тест успешного чтения Excel с использованием patch."""
    mock_exists.return_value = True

    fake_df = pd.DataFrame([
        {"id": 3, "state": "PENDING", "description": "Вклад"}
    ])
    mock_read_excel.return_value = fake_df

    result = load_transactions_from_xlsx("dummy_path.xlsx")

    assert len(result) == 1
    assert result[0]["id"] == 3
    mock_read_excel.assert_called_once_with("dummy_path.xlsx")


@patch("src.csv_xlsx_loader.os.path.exists")
def test_load_xlsx_file_not_found(mock_exists):
    """Тест ситуации, когда XLSX-файл отсутствует на диске."""
    mock_exists.return_value = False
    result = load_transactions_from_xlsx("non_existent.xlsx")
    assert result == []
