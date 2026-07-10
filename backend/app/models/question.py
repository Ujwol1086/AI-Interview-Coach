from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.answer import Answer
    from app.models.interview import Interview


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    interview_id: Mapped[int] = mapped_column(
        ForeignKey("interviews.id"),
        index=True,
    )

    content: Mapped[str] = mapped_column(Text)

    order: Mapped[int] = mapped_column(Integer)

    interview: Mapped["Interview"] = relationship(back_populates="questions")
    answer: Mapped["Answer | None"] = relationship(
        back_populates="question",
        uselist=False,
        cascade="all, delete-orphan",
    )
