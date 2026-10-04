import sys
from pathlib import Path

# Ensure `backend/` is on sys.path when running `fastapi dev main.py` from `app/`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.database import db_connection
from app.api.answers import router as answers_router
from app.api.auth import router as auth_router
from app.api.feedback import evaluate_router, router as feedback_router
from app.api.interviews import router as interviews_router
from app.api.questions import router as questions_router
from app.api.users import router as users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(interviews_router)
app.include_router(questions_router)
app.include_router(answers_router)
app.include_router(feedback_router)
app.include_router(evaluate_router)

@app.get("/")
def home():
    return {"message": "API running"}
