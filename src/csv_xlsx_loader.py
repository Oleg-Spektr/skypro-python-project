import os
from typing import Any, Dict, List

import pandas as pd


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла.

    Возвращает список словарей. Если файл не найден или пуст, возвращает пустой список.
    """
    if not os.path.exists(file_path):
        return []

    try:
        df = pd.read_csv(file_path, sep=";")
        if df.empty:
            return []

        # Заменяем значения NaN на None для корректной типизации
        df = df.astype(object).where(pd.notnull(df), None)
        # Добавляем type ignore, так как mypy сомневается, что ключи DataFrame всегда str
        return df.to_dict(orient="records")  # type: ignore[return-value]
    except (pd.errors.EmptyDataError, pd.errors.ParserError, Exception):
        return []


def load_transactions_from_xlsx(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из XLSX-файла.

    Возвращает список словарей. Если файл не найден или пуст, возвращает пустой список.
    """
    if not os.path.exists(file_path):
        return []

    try:
        df = pd.read_excel(file_path)
        if df.empty:
            return []

        # Заменяем значения NaN на None для корректной типизации
        df = df.astype(object).where(pd.notnull(df), None)
        # Добавляем type ignore для корректного маппинга типов
        return df.to_dict(orient="records")  # type: ignore[return-value]
    except (ValueError, Exception):
        return []
