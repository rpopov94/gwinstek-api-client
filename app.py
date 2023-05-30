import asyncio
import logging
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

from api import app
from gwinstek import init_device


# Init device
async def initialize_device():
    global engine
    engine = await init_device()


# start telemetry trigger

# FastAPI init
app = FastAPI()


# Dataclass
class ChannelData(BaseModel):
    channel: int
    value: float


# API endpoints
@app.post("/set_current")
async def set_current(data: ChannelData):
    try:
        await engine.set_current(data.channel, data.value)
        return {"message": True, "channel": data.channel,  "value": data.value}
    except:
        return {"message": False, "channel": data.channel,  "value": data.value}



@app.post("/set_voltage")
async def set_voltage(data: ChannelData):
    try:
        await engine.set_voltage(data.channel, data.value)
        return {"message": True,  "channel": data.channel,  "value": data.value}
    except:
        return {"message": False, "channel": dat.channel,  "value": data.value}


@app.post("/enable_channel/{channel}")
async def enable_channel(channel: int):
    try:
        await engine.enable_channel(channel)
        return {"channel": channel, "message": True}
    except:
        return {"channel": channel, "message": True}


@app.post("/disable_channel/{channel}")
async def disable_channel(channel: int):
    try:
        await engine.disable_channel(channel)
        return {"message": True, "channel": channel}
    except:
        return {"message": False, "channel": channel}

# не понимаю какой формат будет у сообщения
@app.get("/get_telemetry")
async def get_telemetry():
    telemetry = None
    try:
        telemetry = await engine.get_telemetry()
        return {"message": True, "telemetry": telemetry}
    except:
        return {"message": False, "telemetry": telemetry}


# logging
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(telemetry_polling())


# init log
logging.basicConfig(
    filename="telemetry.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# formatting log messages
def log_telemetry(timestamp, telemetry):
    log_message = f"{timestamp} - {telemetry}"
    logging.info(log_message)


async def telemetry_polling():
    while True:
        telemetry = await engine.get_telemetry()
        timestamp = datetime.now().isoformat()
        log_telemetry(timestamp, telemetry)
        await asyncio.sleep(1)


# trigger for close
@app.on_event("shutdown")
async def shutdown():
    await engine.close()
