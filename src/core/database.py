from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as db:
        yield db