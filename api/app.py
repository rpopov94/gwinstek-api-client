import asyncio
import logging
from datetime import datetime
from fastapi import FastAPI, Depends
import uvicorn
from pydantic import BaseModel

from gwinstek.gwinstek import Gwinstek


app = FastAPI()


# Start trigger
@app.on_event("startup")
async def startup_event():
    async with Gwinstek() as engine:
        app.state.engine = engine
    asyncio.create_task(telemetry_polling())


def get_engine():
    return app.state.engine


class ChannelData(BaseModel):
    channel: int
    value: float


# api endpoints
@app.get("/")
async def home():
    return {"message": "Gwinstek api client"}

@app.post("/set_current")
async def set_current(data: ChannelData, engine=Depends(get_engine)):
    try:
        await engine.set_current(data.channel, data.value)
        return {"message": True, "channel": data.channel, "value": data.value}
    except:
        return {"message": False, "channel": data.channel, "value": data.value}


@app.post("/set_voltage")
async def set_voltage(data: ChannelData, engine=Depends(get_engine)):
    try:
        await engine.set_voltage(data.channel, data.value)
        return {"message": True, "channel": data.channel, "value": data.value}
    except:
        return {"message": False, "channel": data.channel, "value": data.value}


@app.post("/enable_channel/{channel}")
async def enable_channel(channel: int, engine=Depends(get_engine)):
    try:
        await engine.enable_channel(channel)
        return {"channel": channel, "message": True}
    except:
        return {"channel": channel, "message": True}


@app.post("/disable_channel/{channel}")
async def disable_channel(channel: int, engine=Depends(get_engine)):
    try:
        await engine.disable_channel(channel)
        return {"message": True, "channel": channel}
    except:
        return {"message": False, "channel": channel}


@app.get("/get_telemetry")
async def get_telemetry(engine=Depends(get_engine)):
    try:
        telemetry = await engine.get_telemetry()
        return {
            "message": True,
            "telemetry": [float(i) for i in telemetry.split(' ')]
        }
    except:
        return {"message": False, "telemetry": []}


# logging
logging.basicConfig(
    filename="telemetry.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_telemetry(timestamp, telemetry):
    log_message = f"{timestamp} - {telemetry}"
    logging.info(log_message)


async def telemetry_polling():
    while True:
        telemetry = await app.state.engine.get_telemetry()
        timestamp = datetime.now().isoformat()
        log_telemetry(timestamp, telemetry)
        await asyncio.sleep(1)
