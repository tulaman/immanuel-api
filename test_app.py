from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_planetary_positions():
    response = client.get(
        "/planetary_positions?year=1990&month=9&day=5&lat=55.3948&lon=43.8399&hour=15&min=1&sec=53",
        headers={"X-Token": "coneofsilence"},
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["success"] == 1


def test_retrograde_calendar():
    response = client.get(
        "/retrograde_calendar?n=24&lat=55.3948&lon=43.8399",
        headers={"X-Token": "coneofsilence"},
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["success"] == 1
    assert response_json["data"][0]["planet"] == "Mercury"
    assert len(response_json["data"][0]["periods"]) >= 6


def test_get_daily_forecast_data():
    response = client.get(
        "/get_daily_forecast_data?start_date=2024-03-19",
        headers={"X-Token": "coneofsilence"},
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["success"] == 1
    assert len(response_json["data"]) == 3
    assert len(response_json["data"]["planets"]) == 8
    assert "moon_phase" in response_json["data"]
    assert "planets" in response_json["data"]
    assert "aspects" in response_json["data"]
    assert "sign" in response_json["data"]["planets"]["Mercury"]
    assert "house" in response_json["data"]["planets"]["Mercury"]
    assert "movement" in response_json["data"]["planets"]["Mercury"]


def test_get_weekly_forecast_data():
    response = client.get(
        "/get_weekly_forecast_data?start_date=2024-03-19",
        headers={"X-Token": "coneofsilence"},
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["success"] == 1
    assert len(response_json["data"]) == 7
    assert len(response_json["data"]["2024-03-19"]["planets"]) == 8


def test_get_yearly_forecast_data():
    response = client.get(
        "/get_yearly_forecast_data?start_date=2024-04-01",
        headers={"X-Token": "coneofsilence"},
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["success"] == 1
    assert len(response_json["data"]) == 8
    assert len(response_json["data"]["Mercury"]) == 3
    assert "sign" in response_json["data"]["Mercury"]
    assert "movement" in response_json["data"]["Mercury"]
