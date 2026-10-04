from datetime import datetime

from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    answer_id: int
    content: str
    score: int | None = None
    strengths: str | None = None
    improvements: str | None = None


class FeedbackResponse(BaseModel):
    id: int
    answer_id: int
    content: str
    score: int | None
    strengths: str | None
    improvements: str | None
    created_at: datetime

    class Config:
        from_attributes = True
