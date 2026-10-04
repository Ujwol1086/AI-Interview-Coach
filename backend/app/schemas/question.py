from pydantic import BaseModel


class QuestionCreate(BaseModel):
    interview_id: int
    content: str
    order: int


class QuestionResponse(BaseModel):
    id: int
    interview_id: int
    content: str
    order: int

    class Config:
        from_attributes = True
