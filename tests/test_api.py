import pytest
from fastapi.testclient import TestClient
from pytest_mock import mocker

from api.app import app


# Import the pytest-mock fixture
@pytest.fixture
def client(mocker):
    return mocker.Mock(TestClient, app=app)


# Test cases
def test_set_current(client):
    client.post.return_value = mocker.Mock(
        status_code=200,
        json=lambda: {"message": True, "channel": 1, "value": 10.0}
    )

    response = client.post("/set_current", json={"channel": 1, "value": 10.0})

    assert response.status_code == 200
    assert response.json() == {"message": True, "channel": 1, "value": 10.0}


def test_set_voltage(client):
    client.post.return_value = mocker.Mock(
        status_code=200,
        json=lambda: {"message": True, "channel": 2, "value": 5.0}
    )
    response = client.post("/set_voltage", json={"channel": 2, "value": 5.0})
    assert response.status_code == 200
    assert response.json() == {"message": True, "channel": 1, "value": 5.0}


def test_enable_channel(client):
    client.post.return_value = mocker.Mock(
        status_code=200,
        json=lambda: {"message": True}
    )
    response = client.post("/enable_channel",
                           {"message": True, "channel": 4})
    assert response.status_code == 200
    assert response.json() == {"message": True, "channel": 4}


def test_disable_channel(client):
    client.post.return_value = mocker.Mock(
        status_code=200,
        json=lambda: {"message": True, "channel": 4}
    )
    response = client.post("/disable_channel", json={"message": True, "channel": 4})
    assert response.status_code == 200
    assert response.json() == {"message": True, "channel": 4}


def test_get_telemetry(client):
    mock_response_json = {
        "telemetry": [1, 2, 3, 1, 2, 3, 1, 2, 3]
    }
    mocker.patch.object(
        client, "get", return_value=client.Mock(
            status_code=200, json=lambda: mock_response_json))

    response = client.get("/get_telemetry")

    assert response.status_code == 200
    assert isinstance(response.json()["telemetry"], list)
    assert response.json()["telemetry"] == mock_response_json["telemetry"]

