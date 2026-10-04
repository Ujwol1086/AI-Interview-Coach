from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.interview import Interview
from app.models.user import User
from app.schemas.interview import InterviewCreate, InterviewResponse, InterviewUpdate

router = APIRouter(prefix="/interviews", tags=["interviews"])


def get_owned_interview(
    interview_id: int,
    db: Session,
    current_user: User,
) -> Interview:
    interview = (
        db.query(Interview)
        .filter(
            Interview.id == interview_id,
            Interview.user_id == current_user.id,
        )
        .first()
    )
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found",
        )
    return interview


@router.post("/", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
def create_interview(
    interview_data: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    interview = Interview(
        user_id=current_user.id,
        title=interview_data.title,
        status=interview_data.status,
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview


@router.get("/", response_model=list[InterviewResponse])
def list_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Interview)
        .filter(Interview.user_id == current_user.id)
        .order_by(Interview.created_at.desc())
        .all()
    )


@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_interview(interview_id, db, current_user)


@router.patch("/{interview_id}", response_model=InterviewResponse)
def update_interview(
    interview_id: int,
    interview_data: InterviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    interview = get_owned_interview(interview_id, db, current_user)
    updates = interview_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(interview, field, value)

    db.commit()
    db.refresh(interview)
    return interview


@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    interview = get_owned_interview(interview_id, db, current_user)
    db.delete(interview)
    db.commit()
