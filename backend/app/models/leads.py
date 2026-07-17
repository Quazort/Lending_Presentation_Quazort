from datetime import datetime
import enum

from sqlalchemy import String, Text, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class CommentStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    AI_ERROR = 'AI_ERROR'


class LeadModel(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(100))
    user_phone: Mapped[str] = mapped_column(String(20))
    user_email: Mapped[str] = mapped_column(String(255))
    comment: Mapped[str] = mapped_column(Text)
    ai_response: Mapped[str | None] = mapped_column(Text)
    comment_tone: Mapped[str | None] = mapped_column(Text)
    status: Mapped[CommentStatus] = mapped_column(
        Enum(CommentStatus, name="comment_status", native_enum=False),
        default=CommentStatus.SUCCESS)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
