import pytest
from src.widget import mask_account_card, get_date


# === ТЕСТИРОВАНИЕ ФУНКЦИИ mask_account_card ===

@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        # 1. Проверка правильного распознавания типов карт (разные платежные системы)
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Mastercard 1111222233334444", "Mastercard 1111 22** **** 4444"),
        ("Maestro 5555666677778888", "Maestro 5555 66** **** 8888"),

        # 2. Проверка правильного распознавания счетов
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 12345678901234567890", "Счет **7890"),
    ]
)
def test_mask_account_card_positive(input_str: str, expected_output: str) -> None:
    """Универсальный параметризованный тест для корректных типов карт и счетов."""
    assert mask_account_card(input_str) == expected_output


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",  # Абсолютно пустая строка
        "Visa",  # Только название карты без номера
        "123",  # Только короткий номер без типа
        "Невалидный текст",  # Просто случайный текст
    ]
)
def test_mask_account_card_negative(invalid_input: str) -> None:
    """Тестирование функции на обработку некорректных данных и её устойчивость к ошибкам."""
    # Проверяем, что функция не падает с ошибкой (Crash), а возвращает строку
    result = mask_account_card(invalid_input)
    assert isinstance(result, str)


# === ТЕСТИРОВАНИЕ ФУНКЦИИ get_date ===

@pytest.mark.parametrize(
    "date_str, expected_date",
    [
        # 1. Правильность преобразования стандартной даты ISO
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2018-12-31T23:59:59.999999", "31.12.2018"),
    ]
)
def test_get_date_positive(date_str: str, expected_date: str) -> None:
    """Тестирование правильности преобразования валидных форматов даты."""
    assert get_date(date_str) == expected_date


def test_get_date_missing_or_invalid() -> None:
    """Проверка работы функции при отсутствии даты или нестандартном формате."""
    # Перехватываем абсолютно любую ошибку при пустой строке
    with pytest.raises(Exception):
        get_date("")

    # Перехватываем абсолютно любую ошибку при некорректном тексте
    with pytest.raises(Exception):
        get_date("невалидная_дата_123")
