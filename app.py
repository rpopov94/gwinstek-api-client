import asyncio
import logging
from datetime import datetime

from api import app, device
from gwinstek.utils import log_telemetry

# log init
logging.basicConfig(
    filename="telemetry.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(telemetry_polling())


async def telemetry_polling():
    while True:
        telemetry = await device.get_telemetry()
        timestamp = datetime.now().isoformat()
        log_telemetry(timestamp, telemetry)
        await asyncio.sleep(1)
