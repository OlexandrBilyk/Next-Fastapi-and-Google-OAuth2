from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import String
from dotenv import load_dotenv
import os
import bcrypt


load_dotenv()

DB_URL = os.getenv('DB_URL')

Base = declarative_base()

engine = create_async_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    provider: Mapped[str] = mapped_column(String(50))


async def get_db():
    async with SessionLocal() as db:
        yield db
