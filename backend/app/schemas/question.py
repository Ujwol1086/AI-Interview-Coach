from pydantic import BaseModel, Field


class QuestionCreate(BaseModel):
    content: str
    order: int


class QuestionGenerateRequest(BaseModel):
    role: str
    topic: str | None = None
    count: int = Field(default=5, ge=1, le=10)
    difficulty: str = "medium"


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
