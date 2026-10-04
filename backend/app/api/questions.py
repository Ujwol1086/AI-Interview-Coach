from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.interviews import get_owned_interview
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.question import Question
from app.models.user import User
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate

router = APIRouter(
    prefix="/interviews/{interview_id}/questions",
    tags=["questions"],
)


def get_owned_question(
    interview_id: int,
    question_id: int,
    db: Session,
    current_user: User,
) -> Question:
    get_owned_interview(interview_id, db, current_user)
    question = (
        db.query(Question)
        .filter(
            Question.id == question_id,
            Question.interview_id == interview_id,
        )
        .first()
    )
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )
    return question


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(
    interview_id: int,
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_interview(interview_id, db, current_user)

    question = Question(
        interview_id=interview_id,
        content=question_data.content,
        order=question_data.order,
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


@router.get("/", response_model=list[QuestionResponse])
def list_questions(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_interview(interview_id, db, current_user)
    return (
        db.query(Question)
        .filter(Question.interview_id == interview_id)
        .order_by(Question.order.asc())
        .all()
    )


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    interview_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_question(interview_id, question_id, db, current_user)


@router.patch("/{question_id}", response_model=QuestionResponse)
def update_question(
    interview_id: int,
    question_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    question = get_owned_question(interview_id, question_id, db, current_user)
    updates = question_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(question, field, value)

    db.commit()
    db.refresh(question)
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    interview_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    question = get_owned_question(interview_id, question_id, db, current_user)
    db.delete(question)
    db.commit()
