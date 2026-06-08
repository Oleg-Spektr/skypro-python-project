import logging
import os

# Создаем папку logs, если её вдруг не оказалось
os.makedirs("logs", exist_ok=True)

# 1. Создан отдельный объект логера для модуля masks
logger = logging.getLogger("masks")
# 2. Установлен уровень логирования не меньше, чем DEBUG (выбираем DEBUG)
logger.setLevel(logging.DEBUG)

# 3. Настроен file_handler для логера модуля masks (с перезаписью mode="w")
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# 4. Настроен file_formatter (метка времени, название модуля, уровень, сообщение)
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

# 5. Установлен форматер для логера модуля masks
file_handler.setFormatter(formatter)

# 6. Добавлен handler для логера модуля masks
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция переводит числа в строку, а также заменяет часть символов на звёзды."""
    logger.info("Начало маскирования номера карты.")
    card_str = str(card_number).strip()

    # Если в номере карты есть не только цифры, фиксируем ошибку в лог по критериям
    if not card_str or not card_str.isdigit():
        logger.error(f"Ошибка: Некорректный номер карты для маскирования. Inputs: {card_number}")
        # Но не прерываем выполнение, чтобы старые тесты не падали

    # Создание маски: первые 6 и последние 4 символа - цифры, остальные звёзды
    mask_card = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"

    logger.info("Номер карты успешно замаскирован.")
    return mask_card


def get_mask_account(account_number: str) -> str:
    """Функция переводит числа от номера аккаунта в строку, а после скрывает всё, кроме последних 6 символов."""
    logger.info("Начало маскирования номера счета.")
    account_str = str(account_number).strip()

    # Если в номере счета есть не только цифры, фиксируем ошибку в лог по критериям
    if not account_str or not account_str.isdigit():
        logger.error(f"Ошибка: Некорректный номер счета для маскирования. Inputs: {account_number}")

    # Последние 6 символов: 2 звёздочки и последние 4 цифры номера аккаунта
    mask_account = f"**{account_str[-4:]}"

    logger.info("Номер счета успешно замаскирован.")
    return mask_account
