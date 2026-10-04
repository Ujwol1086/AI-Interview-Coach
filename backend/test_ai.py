import asyncio

from app.services.ai_service import get_ai_service


async def main():
    ai_service = get_ai_service()

    questions = await ai_service.generate_questions(
        role="Python Backend Developer",
        topic="FastAPI and REST APIs",
        count=5,
        difficulty="medium",
    )

    for question in questions:
        print(f"{question.order}. {question.content}")


if __name__ == "__main__":
    asyncio.run(main())

