from fastapi import FastAPI
from . import models
from .database import engine
from .routers import transportation, user, authentication
import asyncio

app = FastAPI()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()

app.include_router(transportation.router)
app.include_router(user.router)
app.include_router(authentication.router)
