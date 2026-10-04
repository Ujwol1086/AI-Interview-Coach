"""Gemini implementation of the AIService interface."""

from __future__ import annotations

import json

from google import genai
from google.genai import types

from app.services.ai_service import (
    AIService,
    EvaluationResult,
    GeneratedQuestion,
)

_AFC_DISABLED = types.AutomaticFunctionCallingConfig(disable=True)


class GeminiService(AIService):
    def __init__(self, *, api_key: str, model: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def generate_questions(
        self,
        *,
        role: str,
        topic: str | None = None,
        count: int = 5,
        difficulty: str = "medium",
    ) -> list[GeneratedQuestion]:
        prompt = f"""
You are an expert technical interviewer.

Generate {count} interview questions for a candidate applying for the role:
{role}

Difficulty:
{difficulty}

Topic:
{topic or "General"}

Return ONLY valid JSON in this format:

{{
    "questions": [
        {{
            "content": "Question text",
            "order": 1
        }}
    ]
}}

Rules:
- Generate exactly {count} questions.
- Questions should be relevant to the role.
- Match the requested difficulty.
- Avoid duplicate questions.
- The order must start at 1.
"""

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json",
                system_instruction="You generate structured interview questions.",
                automatic_function_calling=_AFC_DISABLED,
            ),
        )

        content = response.text
        if not content:
            raise RuntimeError("Gemini returned an empty response")

        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Gemini returned invalid JSON for question generation"
            ) from exc

        return [
            GeneratedQuestion.model_validate(question)
            for question in data["questions"]
        ]

    async def evaluate_answer(
        self,
        *,
        question: str,
        answer: str,
        role: str | None = None,
    ) -> EvaluationResult:
        prompt = f"""
You are an expert interview evaluator.

Evaluate the following interview answer.

Role:
{role or "Not specified"}

Question:
{question}

Candidate Answer:
{answer}

Return ONLY valid JSON in this exact format:

{{
    "content": "Overall evaluation of the answer",
    "score": 8,
    "strengths": "What the candidate did well",
    "improvements": "What the candidate should improve"
}}

Rules:
- score must be an integer from 0 to 10.
- Evaluate relevance, clarity, technical correctness,
  structure, and completeness.
- Give specific and constructive feedback.
"""

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                response_mime_type="application/json",
                system_instruction="You are an expert interview answer evaluator.",
                automatic_function_calling=_AFC_DISABLED,
            ),
        )

        content = response.text
        if not content:
            raise RuntimeError("Gemini returned an empty response")

        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Gemini returned invalid JSON for answer evaluation"
            ) from exc

        return EvaluationResult.model_validate(data)
