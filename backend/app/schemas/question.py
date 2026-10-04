from pydantic import BaseModel


class QuestionCreate(BaseModel):
    content: str
    order: int


class QuestionUpdate(BaseModel):
    content: str | None = None
    order: int | None = None


class QuestionResponse(BaseModel):
    id: int
    interview_id: int
    content: str
    order: int

    class Config:
        from_attributes = True
