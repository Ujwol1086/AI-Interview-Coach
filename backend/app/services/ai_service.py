"""Provider-independent AI service interface.

Routers and domain services should depend on `AIService` / `get_ai_service()`
only. Concrete providers (OpenAI, Anthropic, stub, etc.) implement this contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from app.core.config import AI_API_KEY, AI_MODEL, AI_PROVIDER


class GeneratedQuestion(BaseModel):
    content: str
    order: int


class EvaluationResult(BaseModel):
    content: str
    score: int | None = Field(default=None, ge=0, le=10)
    strengths: str | None = None
    improvements: str | None = None


class AIService(ABC):
    """Abstract interface for interview AI capabilities."""

    @abstractmethod
    async def generate_questions(
        self,
        *,
        role: str,
        topic: str | None = None,
        count: int = 5,
        difficulty: str = "medium",
    ) -> list[GeneratedQuestion]:
        """Generate interview questions for a role/topic."""

    @abstractmethod
    async def evaluate_answer(
        self,
        *,
        question: str,
        answer: str,
        role: str | None = None,
    ) -> EvaluationResult:
        """Evaluate a candidate answer and return structured feedback."""


class StubAIService(AIService):
    """Deterministic local provider for development without calling a real API."""

    MAX_QUESTIONS = 5

    async def generate_questions(
        self,
        *,
        role: str,
        topic: str | None = None,
        count: int = 5,
        difficulty: str = "medium",
    ) -> list[GeneratedQuestion]:
        if count < 1:
            raise ValueError("count must be at least 1")
        if count > self.MAX_QUESTIONS:
            raise ValueError(
                f"StubAIService supports at most {self.MAX_QUESTIONS} questions, "
                f"got {count}"
            )

        focus = topic or "general experience"
        templates = [
            f"Tell me about yourself and why you want to work as a {role}.",
            f"Describe a challenging project related to {focus}.",
            f"How do you approach problem-solving as a {role}?",
            f"What is a recent failure you learned from in {focus}?",
            f"Where do you want to grow next as a {role}?",
        ]
        selected = templates[:count]
        return [
            GeneratedQuestion(content=content, order=index)
            for index, content in enumerate(selected, start=1)
        ]

    async def evaluate_answer(
        self,
        *,
        question: str,
        answer: str,
        role: str | None = None,
    ) -> EvaluationResult:
        word_count = len(answer.split())
        score = min(10, max(1, word_count // 10))
        role_label = role or "the role"

        return EvaluationResult(
            content=(
                f"Stub evaluation for {role_label}. "
                f"Your answer to '{question[:80]}' was reviewed locally."
            ),
            score=score,
            strengths="Clear attempt and relevant direction."
            if word_count >= 20
            else "You started answering the question.",
            improvements="Add concrete examples, metrics, and a clearer structure."
            if word_count < 80
            else "Tighten the narrative and highlight measurable impact.",
        )


def get_ai_service() -> AIService:
    """Factory that returns the configured AI provider implementation."""
    provider = (AI_PROVIDER or "stub").strip().lower()

    if provider == "stub":
        return StubAIService()

    if provider == "openai":
        from app.services.providers.openai_provider import OpenAIService

        if not AI_API_KEY:
            raise RuntimeError("AI_API_KEY is required when AI_PROVIDER=openai")
        return OpenAIService(api_key=AI_API_KEY, model=AI_MODEL)

    raise ValueError(
        f"Unsupported AI_PROVIDER '{AI_PROVIDER}'. Use 'stub' or 'openai'."
    )
