import enum
from typing import Annotated, Optional

from pydantic import BaseModel, StringConstraints, EmailStr


class FeedbackRequestSchema(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=20)]
    phone: Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^(?:\+7|8)\d{10}$")]
    email: EmailStr
    comment: Annotated[str, StringConstraints(strip_whitespace=True, min_length=10, max_length=2000)]


class FeedbackResponseSchema(BaseModel):
    status: str = "success"
    message: str = "Feedback received successfully"


class ToneEnum(enum.Enum):
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"

class AIResponseSchema(BaseModel):
    comment_tone: ToneEnum
    response: str
