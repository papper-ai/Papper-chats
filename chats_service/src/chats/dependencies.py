from uuid import UUID

from fastapi import Body
from fastapi.exceptions import HTTPException

from src.database.repositories import ChatRepository


async def chat_exists(chat_id: UUID = Body(...)) -> ChatRepository:
    chat_repository = ChatRepository()

    chat = await chat_repository.get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return chat
