from fastapi import APIRouter
from pydantic import BaseModel

from api import device


# Dataclass
class ChannelData(BaseModel):
    channel: int
    value: float | int


router = APIRouter()


# API endpoints
@router.post("/set_current")
async def set_current(data: ChannelData):
    await device.set_current(data.channel, data.value)
    return {"message": "Current set successfully"}


@router.post("/set_voltage")
async def set_voltage(data: ChannelData):
    await device.set_voltage(data.channel, data.value)
    return {"message": "Voltage set successfully"}


@router.post("/enable_channel/{channel}")
async def enable_channel(channel: int):
    await device.enable_channel(channel)
    return {"message": "Channel enabled"}


@router.post("/disable_channel/{channel}")
async def disable_channel(channel: int):
    await device.disable_channel(channel)
    return {"message": "Channel disabled"}


@router.post("/enable_all_channels")
async def enable_all_channels():
    await device.enable_all_channels()
    return {"message": "All channels enabled"}


@router.post("/disable_all_channels")
async def disable_all_channels():
    await device.disable_all_channels()
    return {"message": "All channels disabled"}


@router.get("/get_telemetry")
async def get_telemetry():
    telemetry = await device.get_telemetry()
    return {"telemetry": telemetry}


@router.get("/get_power/{channel}")
async def get_power(channel: int):
    power = await device.get_power(channel)
    return {"power": power}


@router.get("/get_voltage/{channel}")
async def get_voltage(channel: int):
    voltage = await device.get_voltage(channel)
    return {"voltage": voltage}


@router.get("/get_current/{channel}")
async def get_current(channel: int):
    current = await device.get_current(channel)
    return {"current": current}
