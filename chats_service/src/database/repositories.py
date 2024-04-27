import typing
from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import pool, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.database import models

engine = create_async_engine(
    settings.database_url,
    poolclass=pool.AsyncAdaptedQueuePool,
    pool_size=16,
    max_overflow=4,
    pool_pre_ping=True,
)

Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, entity):
        raise NotImplementedError

    @abstractmethod
    async def get(self, entity_id):
        raise NotImplementedError


class ChatRepository(AbstractRepository):
    def __init__(self):
        self.session = Session()

    async def add(self, entity):
        async with self.session as session:
            async with session.begin():
                session.add(entity)

    async def get(self, id: UUID) -> models.Chat | None:
        async with self.session as session:
            document = await session.get(models.Chat, id)
            return document

    async def delete(self, id: UUID) -> None:
        async with self.session as session:
            async with session.begin():
                сhat = await session.get(models.Chat, id)
                await session.delete(сhat)

    async def set_name(self, id: UUID, name: str) -> None:
        async with self.session as session:
            async with session.begin():
                сhat = await session.get(models.Chat, id)
                if сhat:
                    сhat.name = name

    async def archive(self, id: UUID) -> None:
        async with self.session as session:
            async with session.begin():
                сhat = await session.get(models.Chat, id)
                if сhat:
                    сhat.is_archived = True

    async def unarchive(self, id: UUID) -> None:
        async with self.session as session:
            async with session.begin():
                сhat = await session.get(models.Chat, id)
                if сhat:
                    сhat.is_archived = False

    async def get_users_chats(self, user_id: UUID, archived: bool = False) -> typing.List[models.Chat] | None:
        async with self.session as session:
            chats = await session.execute(
                select(models.Chat).where(models.Chat.user_id == user_id, models.Chat.is_archived == archived)
            )
            return chats.scalars().all()
