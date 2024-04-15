import logging
import uuid
from typing import List

from fastapi import BackgroundTasks, HTTPException

from src.chats.schemas import ChatResponse, CreateChatRequest
from src.database.models import Chat
from src.database.repositories import ChatRepository
from src.utils.requests import (
    send_create_request_to_history_service,
    send_delete_request_to_history_service,
)


async def create_chat(create_chat_request: CreateChatRequest) -> ChatResponse:
    chat_repository = ChatRepository()

    id = uuid.uuid4()  # Generate random unique identifier

    chat = Chat(
        id=id,
        name=create_chat_request.name,
        vault_id=create_chat_request.vault_id,
        user_id=create_chat_request.user_id,
    )

    await chat_repository.add(chat)

    try:
        await send_create_request_to_history_service(chat_id=chat.id)
    except Exception as e:
        logging.error(e)
        await chat_repository.delete(chat.id)
        raise HTTPException(
            status_code=500,
            detail=f"Error creating history for chat {chat.id}",
        )

    # Return the created vault representation
    return ChatResponse.model_validate(chat)


async def delete_history_background(chat_id: uuid.UUID) -> None:
    await send_delete_request_to_history_service(chat_id=chat_id)


async def delete_chat(
    chat_id: uuid.UUID,
    chat_repository: ChatRepository,
    background_tasks: BackgroundTasks,
) -> None:
    await chat_repository.delete(chat_id)
    background_tasks.add_task(delete_history_background, chat_id)


async def set_chat_name(
    chat_id: uuid.UUID, name: str, chat_repository: ChatRepository
) -> None:
    try:
        await chat_repository.set_name(id=chat_id, name=name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting chat name: {e}")


async def get_users_chats(user_id: uuid.UUID) -> List[ChatResponse]:
    chat_repository = ChatRepository()
    chats = await chat_repository.get_users_chats(user_id=user_id)
    return [ChatResponse.model_validate(chat) for chat in chats]


async def get_chat_by_id(
    chat_id: uuid.UUID, chat_repository: ChatRepository
) -> ChatResponse:
    chat = await chat_repository.get(chat_id)
    return ChatResponse.model_validate(chat)
