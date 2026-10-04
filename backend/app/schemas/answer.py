from datetime import datetime

from pydantic import BaseModel


class AnswerCreate(BaseModel):
    question_id: int
    content: str


class AnswerResponse(BaseModel):
    id: int
    question_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
