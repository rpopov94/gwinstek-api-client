import pytest
from unittest.mock import Mock
from gwinstek import Gwinstek
import pyvisa.errors


@pytest.fixture
def mock_device():
    return Mock()


@pytest.fixture
def gwinstek(mock_device):
    return Gwinstek(mock_device)


@pytest.mark.asyncio
async def test_set_current(gwinstek, mock_device):
    channel = 1
    value = 2.5

    await gwinstek.set_current(channel, value)
    mock_device.query_async.assert_called_once_with("ISET1:2.5000")


@pytest.mark.asyncio
async def test_set_voltage(gwinstek, mock_device):
    channel = 2
    value = 12.3

    await gwinstek.set_voltage(channel, value)
    mock_device.query_async.assert_called_once_with("VSET2:12.300")


@pytest.mark.asyncio
async def test_enable_channel(gwinstek, mock_device):
    channel = 1

    await gwinstek.enable_channel(channel)
    mock_device.query_async.assert_called_once_with(":OUTPut1:STATe ON")


@pytest.mark.asyncio
async def test_disable_channel(gwinstek, mock_device):
    channel = 2

    await gwinstek.disable_channel(channel)
    mock_device.query_async.assert_called_once_with(":OUTPut2:STATe OFF")


@pytest.mark.asyncio
async def test_get_telemetry(gwinstek, mock_device):
    mock_device.read_async.return_value = "1.23, 2.45, 3.67, 4.56, 7.89, " \
                                          "0.12, 0, 0, 0, 9.87, 6.54, 3.21"

    telemetry = await gwinstek.get_telemetry()
    mock_device.read_async.assert_called_once_with(":MEASure:ALL?")
    assert telemetry == "1.23, 2.45, 3.67, 4.56, 7.89, 0.12, 0, 0, 0, 9.87," \
                        " 6.54, 3.21"


@pytest.mark.asyncio
async def test_set_current_error_handling(gwinstek, mock_device):
    channel = 5
    value = 3.0
    mock_device.query_async.side_effect = pyvisa.errors.VisaIOError

    with pytest.raises(pyvisa.errors.VisaIOError):
        await gwinstek.set_current(channel, value)
    mock_device.query_async.assert_called_once_with("ISET5:3.0000")
    gwinstek.logger.error.assert_called_once()
