import json
import os
from typing import Any, Dict, List


def get_financial_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Читает данные о транзакциях из JSON-файла и возвращает список словарей.

    Если файл не найден, пуст или содержит некорректную структуру (не список),
    возвращает пустой список.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Проверяем, что корневой элемент JSON — это именно список
        if isinstance(data, list):
            return data
        return []

    except json.JSONDecodeError, TypeError:
        # Если файл пустой или содержит невалидный JSON
        return []
