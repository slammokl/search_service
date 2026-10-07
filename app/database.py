from datetime import date 

from sqlalchemy import ARRAY, Date, Integer, String, Text 
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 

from app.config import settings 

class Base(DeclarativeBase): 
    pass 

class Document(Base): 
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
    text: Mapped[str] = mapped_column(Text, nullable=False) 
    rubrics: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list) 
    created_date: Mapped[date] = mapped_column(Date, nullable=False, index=True) 

engine = create_async_engine(settings.database_url, echo=False, future=True) 
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) 

async def get_session(): 
    async with SessionLocal() as session: 
        yield session 