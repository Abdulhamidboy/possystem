import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging
import asyncio

load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1234@localhost/postgres")


engine = create_async_engine(
    DATABASE_URL,
    echo=True,  
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def test_connection():
    try:
        async with engine.connect() as connection:
            await connection.execute("SELECT 1")
            logger.info("Database connection successful")
    except Exception as e:
        logger.error("Database connection failed")
        logger.exception(e)

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

if __name__ == "__main__":
    asyncio.run(test_connection())
