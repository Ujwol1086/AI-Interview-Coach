from datetime import datetime

from pydantic import BaseModel


class InterviewCreate(BaseModel):
    title: str
    status: str = "pending"


class InterviewResponse(BaseModel):
    id: int
    user_id: int
    title: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
