from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

SUPERUSER_DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost/postgres"

# Database URL fetched from environment variables
DATABASE_URL = SUPERUSER_DATABASE_URL

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Define the base class for models
Base = declarative_base()

from contextlib import asynccontextmanager

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_session():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
