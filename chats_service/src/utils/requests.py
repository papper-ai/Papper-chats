from uuid import UUID

import aiohttp
from fastapi.encoders import jsonable_encoder


async def send_create_request_to_history_service(chat_id: UUID) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://history_service:8000/create_history", json=jsonable_encoder(chat_id)
        ) as response:
            return await response.json()


async def send_delete_request_to_history_service(chat_id: UUID) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            "http://history_service:8000/delete_history", json=jsonable_encoder(chat_id)
        ) as response:
            return await response.json()
