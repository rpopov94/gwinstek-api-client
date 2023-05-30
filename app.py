import asyncio
import logging
from datetime import datetime
from fastapi import FastAPI
import uvicorn

from gwinstek import init_device
from endpoints import router


async def initialize_device():
    global engine
    engine = await init_device()


app = FastAPI()

# Include the router from endpoints.py
app.include_router(router)

# logging
def log_telemetry(timestamp, telemetry):
    log_message = f"{timestamp} - {telemetry}"
    logging.info(log_message)


async def telemetry_polling():
    while True:
        telemetry = await engine.get_telemetry()
        timestamp = datetime.now().isoformat()
        log_telemetry(timestamp, telemetry)
        await asyncio.sleep(1)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(telemetry_polling())


@app.on_event("shutdown")
async def shutdown():
    await engine.close()


if __name__ == "__main__":
    asyncio.run(initialize_device())
    logging.basicConfig(
        filename="telemetry.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)
