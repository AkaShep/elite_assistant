import requests

def test_landing_gear_status():
    url = 'http://localhost:5000/ship-status'
    response = requests.get(url)
    assert response.status_code == 200, "API не отвечает или ошибка HTTP"

    data = response.json()
    assert 'isLandingGearDown' in data, "Ответ не содержит ключа 'isLandingGearDown'"
    assert isinstance(data['isLandingGearDown'], bool), "'isLandingGearDown' должен быть типа bool"

    print(f"Статус шасси (isLandingGearDown): {data['isLandingGearDown']}")
