from datetime import datetime

from pydantic import BaseModel


class InterviewCreate(BaseModel):
    title: str
    status: str = "pending"


class InterviewUpdate(BaseModel):
    title: str | None = None
    status: str | None = None


class InterviewResponse(BaseModel):
    id: int
    user_id: int
    title: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
