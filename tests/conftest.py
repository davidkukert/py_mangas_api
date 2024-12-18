import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from mangas_api.app import app
from mangas_api.db import get_session
from mangas_api.models import table_registry


@pytest.fixture(scope='module')
def engine():
    with PostgresContainer(
        'bitnami/postgresql:16.4.0', driver='psycopg'
    ) as postgres:
        _engine = create_async_engine(postgres.get_connection_url(), echo=True)
        yield _engine


@pytest.fixture(scope='module')
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)
        AsyncSessionLocal = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
        async with AsyncSessionLocal() as session:
            yield session

        await session.rollback()

        async with engine.begin() as conn:
            await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture(scope='module')
async def client(session):
    def get_session_override():
        return session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()
