from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from mangas_api.settings import settings

async_engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():  # pragma: no cover
    async with AsyncSessionLocal() as session:
        yield session


T_Session = Annotated[AsyncSession, Depends(get_session)]
