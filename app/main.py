from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import v1_router
from app.core import scheduler


@asynccontextmanager
async def lifespan(f_app: FastAPI):
    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(v1_router, prefix="/api/v1")
