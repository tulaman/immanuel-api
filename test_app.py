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
    assert response_json['success'] == 1