import json
import logging
import os
from typing import Any, Dict, List

# Создаем папку logs, если её нет
os.makedirs("logs", exist_ok=True)

# Инициализируем логер для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)

# Настраиваем отдельный файл-обработчик
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.INFO)

# Применяем формат записей
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


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
