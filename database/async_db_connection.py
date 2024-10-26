import asyncio

from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

from sqlalchemy.ext.asyncio import (AsyncSession,
                                    async_sessionmaker,
                                    create_async_engine)

from database.async_db_engine_url import db_engine_url
from database.db_models.service_model import Service

# The common Base metamodel used to create models in a separate modules packages
Base = declarative_base()


class AsyncDBConnection:

    def __init__(self, db_url):
        self.db_engine_url = db_url
        self.async_engine = create_async_engine(url=self.db_engine_url,
                                                echo=False)

        self.AsyncSession = async_sessionmaker(bind=self.async_engine,
                                               class_=AsyncSession,
                                               expire_on_commit=False)

        print(type(async_sessionmaker(bind=self.async_engine,
                                      class_=AsyncSession,
                                      expire_on_commit=False)))
        print(AsyncSession)

    async def __aenter__(self):
        self.async_session = self.AsyncSession()
        return self.async_session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.async_session.close()

    async def create_tables(self, base: DeclarativeMeta):
        async with self.async_engine.begin() as session:
            await session.run_sync(base.metadata.create_all(self.async_engine, checkfirst=True))


async_db_connector = AsyncDBConnection(db_url=db_engine_url)
async_db_connector.create_tables(Base)


async def main():

    async with AsyncDBConnection(db_url=db_engine_url) as a_session:
        query = select(Service)
        result = await a_session.execute(query)
        services = result.scalars().all()
        for item in services:
            print(item.name)

asyncio.run(main())
