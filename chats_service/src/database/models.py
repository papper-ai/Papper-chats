from sqlalchemy import UUID, DateTime, String, func, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class Chat(Base):
    __tablename__ = "chats"

    id = mapped_column(UUID(as_uuid=True), primary_key=True)
    name = mapped_column(String, nullable=True)
    vault_id = mapped_column(UUID(as_uuid=True), nullable=False)
    user_id = mapped_column(UUID(as_uuid=True), nullable=False)
    is_archived = mapped_column(Boolean, nullable=False, server_default="false")
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
