from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateChatRequest(BaseModel):
    user_id: UUID
    vault_id: str
    name: str | None


class ChatResponse(BaseModel):
    id: UUID
    name: str
    vault_id: UUID
    user_id: UUID
    is_archived: bool
    created_at: datetime

    class Config:
        from_attributes = True
