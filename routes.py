from fastapi import APIRouter
from pydantic import BaseModel

from app import engine


router = APIRouter()


# Dataclass
class ChannelData(BaseModel):
    channel: int
    value: float


# api endpoints
@router.post("/set_current")
async def set_current(data: ChannelData):
    try:
        await engine.set_current(data.channel, data.value)
        return {"message": True, "channel": data.channel, "value": data.value}
    except:
        return {"message": False, "channel": data.channel, "value": data.value}


@router.post("/set_voltage")
async def set_voltage(data: ChannelData):
    try:
        await engine.set_voltage(data.channel, data.value)
        return {"message": True, "channel": data.channel, "value": data.value}
    except:
        return {"message": False, "channel": data.channel, "value": data.value}


@router.post("/enable_channel/{channel}")
async def enable_channel(channel: int):
    try:
        await engine.enable_channel(channel)
        return {"channel": channel, "message": True}
    except:
        return {"channel": channel, "message": True}


@router.post("/disable_channel/{channel}")
async def disable_channel(channel: int):
    try:
        await engine.disable_channel(channel)
        return {"message": True, "channel": channel}
    except:
        return {"message": False, "channel": channel}


@router.get("/get_telemetry")
async def get_telemetry():
    try:
        telemetry = await engine.get_telemetry()
        return {"message": True,
                "telemetry": [float(i) for i in telemetry.split(' ')]}
    except:
        return {"message": False, "telemetry": []}
