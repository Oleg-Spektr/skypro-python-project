import os
import pytest
from src.decorators import log


# ==================== ТЕСТЫ ВЫВОДА В КОНСОЛЬ (Capsys) ====================

def test_log_console_success(capsys):
    """Проверка логирования успешного выполнения функции в консоль."""
    @log()
    def add(x, y):
        return x + y

    result = add(2, 3)
    assert result == 5

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()
    assert captured.out == "add ok\n"


def test_log_console_error(capsys):
    """Проверка логирования ошибки функции в консоль."""
    @log()
    def divide(x, y):
        return x / y

    # Проверяем, что ошибка пробрасывается дальше
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    # Перехватываем вывод ошибки в консоль
    captured = capsys.readouterr()
    assert captured.out == "divide error: ZeroDivisionError. Inputs: (1, 0), {}\n"


# ==================== ТЕСТЫ ЗАПИСИ В ФАЙЛ ====================

def test_log_file_success():
    """Проверка логирования успешного выполнения функции в файл."""
    test_filename = "test_success_log.txt"

    # Удаляем файл, если он остался от прошлых запусков
    if os.path.exists(test_filename):
        os.remove(test_filename)

    @log(filename=test_filename)
    def multiply(x, y):
        return x * y

    multiply(3, 4)

    # Проверяем содержимое файла
    assert os.path.exists(test_filename)
    with open(test_filename, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "multiply ok\n"

    # Чистим за собой созданный файл
    os.remove(test_filename)


def test_log_file_error():
    """Проверка логирования ошибки функции в файл."""
    test_filename = "test_error_log.txt"

    if os.path.exists(test_filename):
        os.remove(test_filename)

    @log(filename=test_filename)
    def greet(name):
        return "Hello " + name

    with pytest.raises(TypeError):
        greet(None)  # Передаем некорректный тип для сложения со строкой

    # Проверяем содержимое файла
    assert os.path.exists(test_filename)
    with open(test_filename, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "greet error: TypeError. Inputs: (None,), {}\n"

    os.remove(test_filename)
