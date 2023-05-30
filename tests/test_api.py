from fastapi.testclient import TestClient
from main import app


# Create a TestClient instance
client = TestClient(app)


def test_set_current():
    payload = {
        "channel": 1,
        "value": 10.0
    }
    # Send a POST request to the endpoint
    response = client.post("/set_current", json=payload)
    # Assert the response status code and content
    assert response.status_code == 200
    assert response.json() == {"message": True, "channel": 1, "value": 10.0}


def test_set_voltage():
    payload = {
        "channel": 1,
        "value": 10.0
    }
    response = client.post("/set_current", json=payload)
    # Assert the response status code and content
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
    response = client.post("/get_telemetry")
    assert response.status_code == 200
    assert response.json() == {"message": True, "telemetry": "somebody..."}
