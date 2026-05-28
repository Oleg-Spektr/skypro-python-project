import functools
import sys
from typing import Any, Callable, Optional, TypeVar

# Объявляем переменную типа для возвращаемого значения функции
R = TypeVar("R")


def log(filename: Optional[str] = None) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """Декоратор для логирования результатов выполнения функции или возникших ошибок."""

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            try:
                # Попытка выполнить декорируемую функцию
                result = func(*args, **kwargs)

                # Формируем строку успешного выполнения
                log_message = f"{func.__name__} ok\n"

                # Записываем лог в файл или в консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    sys.stdout.write(log_message)

                return result

            except Exception as e:
                # В случае ошибки извлекаем её тип
                error_type = type(e).__name__

                # Формируем строку ошибки по ТЗ
                log_message = f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}\n"

                # Записываем лог в файл или в консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    sys.stdout.write(log_message)

                # Пробрасываем ошибку дальше
                raise e

        return wrapper

    return decorator
