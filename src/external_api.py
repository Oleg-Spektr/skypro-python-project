import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env при импорте модуля
load_dotenv()


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """Принимает на вход транзакцию и возвращает сумму транзакции в рублях (float).

    Если валюта операции USD или EUR, происходит обращение к внешнему API
    для получения текущего курса валют и конвертации.
    """
    try:
        # Безопасно извлекаем сумму и код валюты из вложенного словаря
        amount = float(transaction["operationAmount"]["amount"])
        currency_code = transaction["operationAmount"]["currency"]["code"]
    except (KeyError, ValueError, TypeError):
        # Если структура нарушена или отсутствуют ключи, возвращаем 0.0
        return 0.0

    # Если транзакция уже в рублях, конвертация не требуется
    if currency_code == "RUB":
        return amount

    # Если транзакция в иностранной валюте, выполняем конвертацию через API
    if currency_code in ("USD", "EUR"):
        # Достаем токен доступа, который мы прописали в .env
        api_key = os.environ.get("EXCHANGE_RATES_API_KEY", "")

        url = "https://apilayer.com"
        params = {"to": "RUB", "from": currency_code, "amount": amount}
        headers = {"apikey": api_key}

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)

            # Проверяем успешность сетевого ответа (код 200)
            if response.status_code == 200:
                data = response.json()
                return float(data.get("result", 0.0))
        except requests.RequestException:
            # В случае любых сетевых проблем (таймаут, потеря связи) возвращаем 0.0
            return 0.0

    return 0.0
