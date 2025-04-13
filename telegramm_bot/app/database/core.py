from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from config import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DOMAIN,
    POSTGRES_PORT,
    POSTGRES_DB_NAME,
)


engine = create_async_engine(
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_DOMAIN}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}",
    pool_size=10,
    max_overflow=0,
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
