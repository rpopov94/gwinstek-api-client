import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from gwinstek import engine
from routes import router


@pytest.fixture
def client():
    return TestClient(router)


@pytest.fixture(autouse=True)
def mock_engine():
    mock = MagicMock()
    engine.set_current = mock.set_current
    engine.set_voltage = mock.set_voltage
    engine.enable_channel = mock.enable_channel
    engine.disable_channel = mock.disable_channel
    engine.get_telemetry = mock.get_telemetry
    return mock


def test_set_current_endpoint(client, mock_engine):
    channel = 1
    value = 10.0

    response = client.post(
        "/set_current", json={"channel": channel, "value": value})

    mock_engine.set_current.assert_called_once_with(channel, value)

    assert response.status_code == 200
    assert response.json() == {
        "message": True, "channel": channel, "value": value}


def test_set_voltage_endpoint(client, mock_engine):
    channel = 2
    value = 5.0

    response = client.post(
        "/set_voltage", json={"channel": channel, "value": value})

    mock_engine.set_voltage.assert_called_once_with(channel, value)

    assert response.status_code == 200
    assert response.json() == {
        "message": True, "channel": channel, "value": value}


def test_enable_channel_endpoint(client, mock_engine):
    channel = 3

    response = client.post(f"/enable_channel/{channel}")

    mock_engine.enable_channel.assert_called_once_with(channel)

    assert response.status_code == 200
    assert response.json() == {"channel": channel, "message": True}


def test_disable_channel_endpoint(client, mock_engine):
    channel = 4

    response = client.post(f"/disable_channel/{channel}")

    mock_engine.disable_channel.assert_called_once_with(channel)

    assert response.status_code == 200
    assert response.json() == {"message": True, "channel": channel}


def test_get_telemetry_endpoint(client, mock_engine):
    expected_telemetry = {
        "channel1_voltage": 5.0,
        "channel1_current": 2.0,
        "channel1_power": 10.0,
        "channel2_voltage": 3.0,
        "channel2_current": 1.0,
        "channel2_power": 3.0,
        "channel3_voltage": 3.0,
        "channel3_current": 1.0,
        "channel3_power": 3.0,
        "channel4_voltage": 3.0,
        "channel4_current": 1.0,
        "channel4_power": 3.0,
    }

    mock_engine.get_telemetry.return_value = expected_telemetry

    response = client.get("/get_telemetry")

    mock_engine.get_telemetry.assert_called_once()

    assert response.status_code == 200
    assert response.json() == {
        "message": True, "telemetry": expected_telemetry}
