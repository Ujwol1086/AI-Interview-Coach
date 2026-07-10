from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.answer import Answer


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    answer_id: Mapped[int] = mapped_column(
        ForeignKey("answers.id"),
        unique=True,
        index=True,
    )

    score: Mapped[int | None] = mapped_column(Integer)

    content: Mapped[str] = mapped_column(Text)

    strengths: Mapped[str | None] = mapped_column(Text)

    improvements: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    answer: Mapped["Answer"] = relationship(back_populates="feedback")
