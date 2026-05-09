from homework.src.processing import filter_by_state, sort_by_date

# Тестовые данные
data = [
    {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

def test_processing():
    # 1. Тест фильтрации по умолчанию (EXECUTED)
    filtered_executed = filter_by_state(data)
    assert len(filtered_executed) == 2
    assert filtered_executed[0]['state'] == 'EXECUTED'
    print("Тест filter_by_state (default) пройден!")

    # 2. Тест фильтрации по статусу CANCELED
    filtered_canceled = filter_by_state(data, 'CANCELED')
    assert len(filtered_canceled) == 2
    assert filtered_canceled[0]['state'] == 'CANCELED'
    print("Тест filter_by_state (CANCELED) пройден!")

    # 3. Тест сортировки по дате (по убыванию - по умолчанию)
    sorted_data = sort_by_date(data)
    assert sorted_data[0]['id'] == 414288290  # Самая свежая дата (2019 год)
    print("Тест sort_by_date (descending) пройден!")

    # 4. Тест сортировки по дате (по возрастанию)
    sorted_data_asc = sort_by_date(data, descending=False)
    assert sorted_data_asc[0]['id'] == 939719570  # Самая старая дата (июнь 2018)
    print("Тест sort_by_date (ascending) пройден!")

if __name__ == "__main__":
    try:
        test_processing()
        print("\nВсе тесты успешно завершены!")
    except AssertionError as e:
        print(f"\nОшибка в тестах!")