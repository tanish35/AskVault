from fastapi import FastAPI
from contextlib import asynccontextmanager

from routes import file_routes
from lib.config import settings
from prisma import Prisma

prisma = Prisma()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(file_routes.router, prefix="/api/file")
