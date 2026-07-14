from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.config import settings
from app.database import AsyncSessionLocal
from app.dependencies import close_redis, init_redis
from app.models.app_config import AppConfig
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(AppConfig).where(AppConfig.id == 1))
        if result.scalar_one_or_none() is None:
            session.add(AppConfig(id=1, registration_count=0))
            await session.commit()
    yield
    await close_redis()


app = FastAPI(
    title="Baithak API",
    version="0.2.0",
    description="Baithak registration and auth API",
    lifespan=lifespan,
)

origins = [origin.strip() for origin in settings.FRONTEND_URL.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
