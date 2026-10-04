from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("Database connected successfully")
    except Exception as e:
        print(f"Database connection failed: {e}")