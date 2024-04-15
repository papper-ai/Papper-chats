from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Body, Depends, status

from src.chats.dependencies import chat_exists
from src.chats.schemas import ChatResponse, CreateChatRequest
from src.chats.utils import create_chat, delete_chat, get_users_chats, set_chat_name, get_chat_by_id
from src.database.repositories import ChatRepository

chats_router = APIRouter(tags=["Chats"])


@chats_router.post(
    "/create_chat", status_code=status.HTTP_201_CREATED, response_model=ChatResponse
)
async def create_chat_route(
    create_chat_request: Annotated[CreateChatRequest, Body(...)],
):
    return await create_chat(create_chat_request)


@chats_router.delete("/delete_chat", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_route(
    chat_id: Annotated[UUID, Body(...)],
    chat_repository: Annotated[ChatRepository, Depends(chat_exists)],
    background_tasks: BackgroundTasks,
):
    await delete_chat(chat_id, chat_repository, background_tasks)


@chats_router.put("/set_chat_name", status_code=status.HTTP_200_OK)
async def set_chat_name_route(
    chat_id: Annotated[UUID, Body(...)],
    name: Annotated[str, Body(...)],
    chat_repository: Annotated[ChatRepository, Depends(chat_exists)],
):
    await set_chat_name(chat_id, name, chat_repository)


@chats_router.post(
    "/get_users_chats",
    status_code=status.HTTP_200_OK,
    response_model=List[ChatResponse],
)
async def get_users_chats_route(user_id: Annotated[UUID, Body(...)]):
    return await get_users_chats(user_id)


@chats_router.post(
    "/get_chat_by_id",
    status_code=status.HTTP_200_OK,
    response_model=ChatResponse,
)
async def get_chat_by_id_route(
    chat_id: Annotated[UUID, Body(...)],
    chat_repository: Annotated[ChatRepository, Depends(chat_exists)],
):  
    return await get_chat_by_id(chat_id, chat_repository)
    