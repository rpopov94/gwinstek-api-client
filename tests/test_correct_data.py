import logging
import pytest
from pyvisa.errors import VisaIOError

from gwinstek.gwinstek import Gwinstek


# Mocking pyvisa's ResourceManager and Resource classes for testing
class MockResourceManager:
    def open_resource(self, resource_name):
        return MockResource()


class MockResource:
    def __init__(self):
        self.read_termination = '\n'
        self.write_termination = '\n'

    async def query_async(self, command):
        if command.startswith("ISET"):
            return "Set current successful"
        elif command.startswith("VSET"):
            return "Set voltage successful"
        elif command.startswith(":OUTPut"):
            return "Set output successful"
        elif command.startswith(":MEASure"):
            return "Get telemetry successful"
        else:
            return ""

    async def read_async(self, command):
        return "Telemetry values"


@pytest.fixture
async def gwinstek():
    async with Gwinstek(MockResourceManager()) as gw:
        yield gw


@pytest.mark.asyncio
async def test_set_current(gwinstek):
    await gwinstek.set_current(1, 2.5)
    # Assert that the logger has recorded the correct message
    assert logging.info.call_args[0][0] == "Set 2.5 A for channel #1"


@pytest.mark.asyncio
async def test_set_voltage(gwinstek):
    await gwinstek.set_voltage(2, 3.5)
    # Assert that the logger has recorded the correct message
    assert logging.info.call_args[0][0] == "Set 3.5 V for channel #2"


@pytest.mark.asyncio
async def test_enable_channel(gwinstek):
    await gwinstek.enable_channel(3)
    # Assert that the logger has recorded the correct message
    assert logging.info.call_args[0][0] == "Enable channel #3"


@pytest.mark.asyncio
async def test_disable_channel(gwinstek):
    await gwinstek.disable_channel(4)
    # Assert that the logger has recorded the correct message
    assert logging.info.call_args[0][0] == "Disable channel #4"


@pytest.mark.asyncio
async def test_get_telemetry(gwinstek):
    telemetry = await gwinstek.get_telemetry()
    # Assert that the returned telemetry is correct
    assert telemetry == "Telemetry values"


@pytest.mark.asyncio
async def test_set_current_error(gwinstek):
    with pytest.raises(VisaIOError):
        await gwinstek.set_current(1, 2.5)
    # Assert that the logger has recorded the correct error message
    assert logging.error.call_args[0][0].startswith("Error while setting current channel 1")


@pytest.mark.asyncio
async def test_set_voltage_error(gwinstek):
    with pytest.raises(VisaIOError):
        await gwinstek.set_voltage(2, 3.5)
    # Assert that the logger has recorded the correct error message
    assert logging.error.call_args[0][0].startswith("Error while setting voltage:")


@pytest.mark.asyncio
async def test_enable_channel_error(gwinstek):
    with pytest.raises(VisaIOError):
        await gwinstek.enable_channel(3)
    # Assert that the logger has recorded the correct error message
    assert logging.error.call_args[0][0].startswith("Error enable channel #3")


@pytest.mark.asyncio
async def test_disable_channel_error(gwinstek):
    with pytest.raises(VisaIOError):
        await gwinstek.disable_channel(4)
    # Assert that the logger has recorded the correct error message
    assert logging.error.call_args[0][0].startswith("Error disable channel #4")


@pytest.mark.asyncio
async def test_get_telemetry_error(gwinstek):
    with pytest.raises(VisaIOError):
        await gwinstek.get_telemetry()
    # Assert that the logger has recorded the correct error message
    assert logging.error.call_args[0][0].startswith("Error while get telemetry")


# Mocking the logging module
@pytest.fixture(autouse=True)
def mock_logging(mocker):
    mocker.patch("logging.getLogger")
    logger = mocker.Mock()
    logger.error = mocker.Mock()
    logger.info = mocker.Mock()
    logging.getLogger.return_value = logger


