from sqlmodel import SQLModel, create_engine, Session
from sqlmodel import Field, SQLModel
from typing import Optional
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./healthbot.db")
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
