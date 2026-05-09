# Импорт модуля datetime и функций из masks.py
from datetime import datetime

from homework.src.masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> str:
    """Функция маскирует номер карты или счета с защитой от некорректного ввода."""
    if not data:
        return "Некорректный ввод: строка пуста"

    parts = data.split()

    if len(parts) < 2:
        return "Некорректный формат: отсутствуют имя или номер"

    if len(parts) > 4:  # Если слов слишком много
        return "Некорректный формат"

    name = " ".join(parts[:-1])
    number = parts[-1]

    if "счет" in name.lower():
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


# Функция связанная с датой
def get_date(date_str: str) -> str:
    """Функция возвращает дату в формате ДД.ММ.ГГГГ, используя модуль datetime."""
    date_obj = datetime.fromisoformat(date_str)
    return date_obj.strftime("%d.%m.%Y")
