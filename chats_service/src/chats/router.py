from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Body, Depends, status

from src.chats.dependencies import chat_exists
from src.chats.schemas import ChatResponse, CreateChatRequest
from src.chats.utils import (
    archive_chat,
    create_chat,
    delete_chat,
    get_chat_by_id,
    get_user_archived_chats,
    get_user_chats,
    get_vault_chats,
    set_chat_name,
    unarchive_chat,
)
from src.database.repositories import ChatRepository

chats_router = APIRouter(tags=["Chats"])


@chats_router.post(
    "/create_chat", status_code=status.HTTP_201_CREATED, response_model=ChatResponse
)
async def create_chat_route(
    create_chat_request: Annotated[CreateChatRequest, Body()],
):
    return await create_chat(create_chat_request)


@chats_router.delete("/delete_chat", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_route(
    chat_id: Annotated[UUID, Body(embed=True)],
    chat_repository: Annotated[ChatRepository, Depends(chat_exists)],
) -> None:
    await delete_chat(chat_id, chat_repository)


@chats_router.patch("/set_chat_name", status_code=status.HTTP_202_ACCEPTED)
async def set_chat_name_route(
    chat_id: Annotated[UUID, Body()],
    name: Annotated[str, Body()],
    chat_repository: Annotated[ChatRepository, Depends(chat_exists)],
) -> None:
    await set_chat_name(chat_id, name, chat_repository)


@chats_router.post(
    "/get_user_chats",
    status_code=status.HTTP_200_OK,
    response_model=List[ChatResponse],
)
async def get_user_chats_route(user_id: Annotated[UUID, Body(embed=True)]):
    """Получить неархивированные чаты пользователя"""

    return await get_user_chats(user_id)


@chats_router.post(
    "/get_user_archived_chats",
    status_code=status.HTTP_200_OK,
    response_model=List[ChatResponse],
)
async def get_user_archived_chats_route(user_id: Annotated[UUID, Body(embed=True)]):
    """Получить архивированные чаты пользователя"""

    return await get_user_archived_chats(user_id)


@chats_router.post(
    "/get_chat_by_id",
    status_code=status.HTTP_200_OK,
    response_model=ChatResponse,
)
async def get_chat_by_id_route(
    chat_id: Annotated[UUID, Body(embed=True)],
    chat_repository: Annotated[ChatRepository, Depends(chat_exists)],
):
    return await get_chat_by_id(chat_id, chat_repository)


@chats_router.patch("/archive_chat", status_code=status.HTTP_200_OK)
async def archive_chat_route(
    chat_id: Annotated[UUID, Body(embed=True)],
    chat_repository: Annotated[ChatRepository, Depends(chat_exists)],
) -> None:
    await archive_chat(chat_id, chat_repository)


@chats_router.patch("/unarchive_chat", status_code=status.HTTP_200_OK)
async def unarchive_chat_route(
    chat_id: Annotated[UUID, Body(embed=True)],
    chat_repository: Annotated[ChatRepository, Depends(chat_exists)],
) -> None:
    await unarchive_chat(chat_id, chat_repository)


@chats_router.post(
    "/get_vault_chats",
    status_code=status.HTTP_200_OK,
    response_model=List[ChatResponse],
)
async def get_vault_chats_route(
    vault_id: Annotated[UUID, Body(embed=True)],
) -> None:
    return await get_vault_chats(vault_id)
