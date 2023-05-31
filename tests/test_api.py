from fastapi.testclient import TestClient

from api.app import app


# Create a TestClient instance
client = TestClient(app)


# tets set
def test_set_current():
    payload = {
        "channel": 1,
        "value": 10.0
    }
    response = client.post("/set_current", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": True, "channel": 1, "value": 10.0}


def test_set_voltage():
    payload = {
        "channel": 1,
        "value": 10.0
    }
    response = client.post("/set_current", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": True, "channel": 1, "value": 5.0}


def test_enable_channel():
    payload = {
        "channel": 4
    }
    response = client.post("/enable_channel", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": True, "channel": 4}


def test_disable_channel():
    payload = {
        "channel": 4
    }
    response = client.post("/disable_channel", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": True, "channel": 4}


def get_telemetry():
    response = client.get("/get_telemetry")
    assert response.status_code == 200
    assert isinstance(response.json()["telemetry"], list)
