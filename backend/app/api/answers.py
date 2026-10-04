from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.questions import get_owned_question
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.answer import Answer
from app.models.user import User
from app.schemas.answer import AnswerCreate, AnswerResponse, AnswerUpdate

router = APIRouter(
    prefix="/interviews/{interview_id}/questions/{question_id}/answers",
    tags=["answers"],
)


def get_owned_answer(
    interview_id: int,
    question_id: int,
    db: Session,
    current_user: User,
) -> Answer:
    get_owned_question(interview_id, question_id, db, current_user)
    answer = (
        db.query(Answer)
        .filter(Answer.question_id == question_id)
        .first()
    )
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found",
        )
    return answer


@router.post("/", response_model=AnswerResponse, status_code=status.HTTP_201_CREATED)
def create_answer(
    interview_id: int,
    question_id: int,
    answer_data: AnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_question(interview_id, question_id, db, current_user)

    existing = db.query(Answer).filter(Answer.question_id == question_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Answer already exists for this question",
        )

    answer = Answer(
        question_id=question_id,
        content=answer_data.content,
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


@router.get("/", response_model=AnswerResponse)
def get_answer(
    interview_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_answer(interview_id, question_id, db, current_user)


@router.patch("/", response_model=AnswerResponse)
def update_answer(
    interview_id: int,
    question_id: int,
    answer_data: AnswerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    answer = get_owned_answer(interview_id, question_id, db, current_user)
    updates = answer_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(answer, field, value)

    db.commit()
    db.refresh(answer)
    return answer


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
    interview_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    answer = get_owned_answer(interview_id, question_id, db, current_user)
    db.delete(answer)
    db.commit()
