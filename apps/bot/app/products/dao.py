import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from const import asyncpg_url

engine = create_async_engine(url=asyncpg_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def find_product_by_artikul(artikul: int):
    async with async_session_maker() as session:
        query = text("SELECT * FROM products WHERE artikul = :artikul")
        result = await session.execute(query, {"artikul": artikul})
        product = result.fetchone()
        return product
