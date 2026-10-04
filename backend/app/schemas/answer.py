from datetime import datetime

from pydantic import BaseModel


class AnswerCreate(BaseModel):
    content: str


class AnswerUpdate(BaseModel):
    content: str | None = None


class AnswerResponse(BaseModel):
    id: int
    question_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
