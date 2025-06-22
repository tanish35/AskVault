from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from lib.config import settings
from engine import db

from routes import file_routes, user_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(file_routes.router, prefix="/api/file")
app.include_router(user_routes.router, prefix="/api/user")


@app.get("/")
async def root():
    return {"message": "Welcome to the AskVault API"}
