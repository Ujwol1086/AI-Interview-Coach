from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.feedback import Feedback
    from app.models.question import Question


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"),
        unique=True,
        index=True,
    )

    content: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    question: Mapped["Question"] = relationship(back_populates="answer")
    feedback: Mapped["Feedback | None"] = relationship(
        back_populates="answer",
        uselist=False,
        cascade="all, delete-orphan",
    )
