from sqlalchemy.orm import Session

from app.models.answer import Answer
from app.models.feedback import Feedback
from app.services.ai_service import get_ai_service


async def evaluate_and_save_feedback(
    db: Session,
    *,
    answer: Answer,
    role: str | None = None,
) -> Feedback:
    ai = get_ai_service()
    result = await ai.evaluate_answer(
        question=answer.question.content,
        answer=answer.content,
        role=role,
    )

    feedback = Feedback(
        answer_id=answer.id,
        content=result.content,
        score=result.score,
        strengths=result.strengths,
        improvements=result.improvements,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback
