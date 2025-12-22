# backend/db/database.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import redis.asyncio as redis
from core.config import settings

# --- PostgreSQL ---
engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

# --- Redis ---
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


# Dependency для FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session


# Создание таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
