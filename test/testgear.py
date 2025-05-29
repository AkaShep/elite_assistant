import requests

def test_landing_gear_status_with_print():
    url = 'http://localhost:5000/ship-status'
    response = requests.get(url)
    assert response.status_code == 200, "API не отвечает или ошибка HTTP"

    data = response.json()
    assert 'isLandingGearDown' in data, "Ответ не содержит ключа 'isLandingGearDown'"

    is_landing_gear_down = data['isLandingGearDown']

    print("\n=== РЕЗУЛЬТАТ ТЕСТА ===")
    if is_landing_gear_down:
        print("✅ Шасси выпущены!")
    else:
        print("✅ Шасси скрыты!")
    print("=======================\n")
