from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.api.answers import get_owned_answer
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.answer import Answer
from app.models.feedback import Feedback
from app.models.question import Question
from app.models.user import User
from app.schemas.feedback import FeedbackResponse
from app.services.feedback_service import evaluate_and_save_feedback

router = APIRouter(
    prefix="/interviews/{interview_id}/questions/{question_id}/answers/feedback",
    tags=["feedback"],
)

evaluate_router = APIRouter(prefix="/answers", tags=["feedback"])


def get_owned_feedback(
    interview_id: int,
    question_id: int,
    db: Session,
    current_user: User,
) -> Feedback:
    answer = get_owned_answer(interview_id, question_id, db, current_user)
    feedback = (
        db.query(Feedback)
        .filter(Feedback.answer_id == answer.id)
        .first()
    )
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found",
        )
    return feedback


def get_owned_answer_by_id(
    answer_id: int,
    db: Session,
    current_user: User,
) -> Answer:
    answer = (
        db.query(Answer)
        .options(joinedload(Answer.question).joinedload(Question.interview))
        .filter(Answer.id == answer_id)
        .first()
    )
    if not answer or answer.question.interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found",
        )
    return answer


@router.get("/", response_model=FeedbackResponse)
def get_feedback(
    interview_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_feedback(interview_id, question_id, db, current_user)


@evaluate_router.post(
    "/{answer_id}/evaluate",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
async def evaluate_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    answer = get_owned_answer_by_id(answer_id, db, current_user)

    existing = db.query(Feedback).filter(Feedback.answer_id == answer.id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Feedback already exists for this answer",
        )

    try:
        return await evaluate_and_save_feedback(
            db,
            answer=answer,
            role=answer.question.interview.title,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI evaluation failed: {exc}",
        ) from exc
