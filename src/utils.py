import json
import logging
import os
from typing import Any, Dict, List

# Создаем папку logs, если её нет
os.makedirs("logs", exist_ok=True)

# 1. Создан отдельный объект логера для модуля utils
logger = logging.getLogger("utils")
# 2. Установлен уровень логирования не меньше, чем DEBUG (выбираем DEBUG)
logger.setLevel(logging.DEBUG)

# 3. Настроен file_handler для логера модуля utils (с перезаписью mode="w")
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# 4. Настроен file_formatter (метка времени, название модуля, уровень, сообщение)
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

# 5. Установлен форматер для логера модуля utils
file_handler.setFormatter(formatter)

# 6. Добавлен handler для логера модуля utils
logger.addHandler(file_handler)


def get_financial_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Читает данные о транзакциях из JSON-файла и возвращает список словарей.

    Если файл не найден, пуст или содержит некорректную структуру (не список),
    возвращает пустой список.
    """
    # Логируем успешное начало выполнения функции
    logger.info(f"Запущено чтение финансовых транзакций из файла: {file_path}")

    if not os.path.exists(file_path):
        # Логируем ошибочный случай (файл не найден) с уровнем ERROR
        logger.error(f"Ошибка: Файл {file_path} не найден на диске.")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Проверяем, что корневой элемент JSON — это именно список
        if isinstance(data, list):
            # Логируем успешное завершение чтения с указанием количества транзакций
            logger.info(f"Успешно прочитано транзакций: {len(data)}")
            return data

        # Логируем ошибочный случай: структура JSON не является списком
        logger.error(f"Ошибка: Структура данных в файле {file_path} не является списком.")
        return []

    except (json.JSONDecodeError, TypeError) as e:
        # Логируем критические ошибки разбора (пустой файл или битый JSON) с уровнем ERROR
        logger.error(f"Ошибка: Не удалось прочитать JSON из файла {file_path}. Детали: {e}")
        return []
