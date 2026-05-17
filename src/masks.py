def get_mask_card_number(card_number: str) -> str:
    """Функция переводит числа в строку, а также заменяет часть символов на звёзды"""
    card_str = str(card_number)

    # Создание маски: первые 6 и последние 4 символа - цифры, остальные звёзды
    mask_card = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"

    return mask_card


# Пример работы:
print(get_mask_card_number("7000792289606361"))  # 7000792289606361 - входной аргумент
# Вывод функции - 7000 79** **** 6361


def get_mask_account(account_number: str) -> str:
    """Функция переводит числа от номера аккаунта в строку, а после скрывает всё, кроме последних 6 символов"""
    account_str = str(account_number)

    # Последние 6 символов: 2 звёздочки и последние 4 цифры номера аккаунта
    mask_account = f"**{account_str[-4:]}"

    return mask_account


# Пример работы:
print(get_mask_account("73654108430135874305"))
# Вывод функции - **4305
