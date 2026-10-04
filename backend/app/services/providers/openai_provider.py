"""OpenAI implementation of the AIService interface.

Methods are scaffolded here so the rest of the app can stay provider-agnostic.
Wire the actual API calls in a follow-up step.
"""

from __future__ import annotations

from app.services.ai_service import AIService, EvaluationResult, GeneratedQuestion


class OpenAIService(AIService):
    def __init__(self, *, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    async def generate_questions(
        self,
        *,
        role: str,
        topic: str | None = None,
        count: int = 5,
        difficulty: str = "medium",
    ) -> list[GeneratedQuestion]:
        raise NotImplementedError(
            "OpenAI question generation is not implemented yet"
        )

    async def evaluate_answer(
        self,
        *,
        question: str,
        answer: str,
        role: str | None = None,
    ) -> EvaluationResult:
        raise NotImplementedError(
            "OpenAI answer evaluation is not implemented yet"
        )
