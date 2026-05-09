from homework.src.processing import filter_by_state, sort_by_date

# Тестовые данные разбиваем на несколько строк, чтобы уложиться в 79 символов
data = [
    {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


def test_processing() -> None:
    """Тестирование функций обработки данных."""
    # 1. Тест фильтрации по умолчанию (EXECUTED)
    filtered_executed = filter_by_state(data)
    assert len(filtered_executed) == 2
    for item in filtered_executed:
        assert item["state"] == "EXECUTED"
    print("Тест filter_by_state (default) пройден!")

    # 2. Тест фильтрации по статусу CANCELED
    filtered_canceled = filter_by_state(data, "CANCELED")
    assert len(filtered_canceled) == 2
    for item in filtered_canceled:
        assert item["state"] == "CANCELED"
    print("Тест filter_by_state (CANCELED) пройден!")

    # 3. Тест сортировки по дате (по убыванию)
    sorted_data = sort_by_date(data)
    assert sorted_data[0]["id"] == 414288290
    print("Тест sort_by_date (descending) пройден!")


if __name__ == "__main__":
    test_processing()
    print("\nВсе тесты успешно завершены!")
