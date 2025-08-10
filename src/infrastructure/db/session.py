from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config.settings import settings

engine = create_async_engine(settings.db_url)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
