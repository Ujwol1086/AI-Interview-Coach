import sys
from pathlib import Path

# Ensure `backend/` is on sys.path when running `fastapi dev main.py` from `app/`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import db_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "API running"}