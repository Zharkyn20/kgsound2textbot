from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger

import handlers
from routes import root_router
from settings import get_settings
from dotenv import load_dotenv


load_dotenv()
cfg = get_settings()


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("🚀 Starting application")
    from bot import start_telegram
    await start_telegram()
    yield
    logger.info("⛔ Stopping application")

app = FastAPI(lifespan=lifespan)
app.include_router(root_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=443)
