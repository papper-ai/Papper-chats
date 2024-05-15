import uuid
from typing import List

from fastapi import HTTPException

from src.chats.schemas import ChatResponse, CreateChatRequest
from src.database.models import Chat
from src.database.repositories import ChatRepository


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

    # Return the created vault representation
    return ChatResponse.model_validate(chat)


async def delete_chat(
    chat_id: uuid.UUID,
    chat_repository: ChatRepository,
) -> None:
    await chat_repository.delete(chat_id)


async def set_chat_name(
    chat_id: uuid.UUID, name: str, chat_repository: ChatRepository
) -> ChatResponse:
    try:
        await chat_repository.set_name(id=chat_id, name=name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting chat name: {e}")


async def get_user_chats(user_id: uuid.UUID) -> List[ChatResponse]:
    chat_repository = ChatRepository()
    chats = await chat_repository.get_user_chats(user_id=user_id, archived=False)

    return [ChatResponse.model_validate(chat) for chat in chats]


async def get_vault_chats(vault_id: uuid.UUID) -> List[ChatResponse]:
    chat_repository = ChatRepository()
    chats = await chat_repository.get_vault_chats(vault_id=vault_id)

    return [ChatResponse.model_validate(chat) for chat in chats]


async def get_user_archived_chats(user_id: uuid.UUID) -> List[ChatResponse]:
    chat_repository = ChatRepository()
    chats = await chat_repository.get_user_chats(user_id=user_id, archived=True)

    return [ChatResponse.model_validate(chat) for chat in chats]


async def get_chat_by_id(
    chat_id: uuid.UUID, chat_repository: ChatRepository
) -> ChatResponse:
    chat = await chat_repository.get(chat_id)
    return ChatResponse.model_validate(chat)


async def archive_chat(
    chat_id: uuid.UUID, chat_repository: ChatRepository
) -> ChatResponse:
    await chat_repository.archive(chat_id)


async def unarchive_chat(
    chat_id: uuid.UUID, chat_repository: ChatRepository
) -> ChatResponse:
    await chat_repository.unarchive(chat_id)
