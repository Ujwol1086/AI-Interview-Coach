from sqlalchemy.orm import Session

from app.models.question import Question
from app.services.ai_service import get_ai_service


async def generate_questions_for_interview(
    db: Session,
    *,
    interview_id: int,
    role: str,
    topic: str | None = None,
    count: int = 5,
    difficulty: str = "medium",
) -> list[Question]:
    ai = get_ai_service()
    generated = await ai.generate_questions(
        role=role,
        topic=topic,
        count=count,
        difficulty=difficulty,
    )

    existing_count = (
        db.query(Question)
        .filter(Question.interview_id == interview_id)
        .count()
    )

    questions: list[Question] = []
    for item in generated:
        question = Question(
            interview_id=interview_id,
            content=item.content,
            order=existing_count + item.order,
        )
        db.add(question)
        questions.append(question)

    db.commit()
    for question in questions:
        db.refresh(question)

    return questions
