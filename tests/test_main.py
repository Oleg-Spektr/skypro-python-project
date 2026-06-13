from src.main import main


def test_main_scenario_success(monkeypatch, capsys):
    """Тестирует успешный сценарий выполнения функции main."""
    # Имитируем последовательные ответы пользователя в консоли
    inputs = [
        "1",  # Выбор JSON-файла
        "executed",  # Выбор статуса (в нижнем регистре для проверки приведения)
        "да",  # Отсортировать по дате?
        "по убыванию",  # Порядок сортировки
        "нет",  # Выводить только рублевые? (ставим нет, чтобы не обнулить тестовый список)
        "нет",  # Отфильтровать по слову в описании?
    ]

    # Подменяем стандартный input нашим списком ответов
    iterator = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(iterator))

    # Запускаем главную функцию
    main()

    # Перехватываем вывод в консоль для проверок
    captured = capsys.readouterr().out

    # Проверяем, что ключевые сообщения отобразились корректно
    assert "Для обработки выбран JSON-файл" in captured
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in captured
    assert "Всего банковских операций в выборке: 4" in captured


def test_main_invalid_file_choice(monkeypatch, capsys):
    """Тест ситуации, когда пользователь ввел неверный пункт меню файлов."""
    monkeypatch.setattr("builtins.input", lambda _: "5")

    main()

    captured = capsys.readouterr().out
    assert "Некорректный выбор" in captured


def test_main_empty_result_by_word(monkeypatch, capsys):
    """Тест сценария, когда фильтр по слову оставляет выборку пустой."""
    inputs = ["1", "executed", "нет", "нет", "да", "несуществующее_слово"]
    iterator = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(iterator))

    main()

    captured = capsys.readouterr().out
    assert "Не найдено ни одной транзакции" in captured
