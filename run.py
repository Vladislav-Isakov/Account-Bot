import asyncio
import os
import sys
from bot.models import Base
from bot import async_engine


if __name__ == '__main__':
    async def main():
        async def create_tables():
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)
        await create_tables()

asyncio.run(main())