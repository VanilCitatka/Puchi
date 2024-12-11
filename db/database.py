from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

SQLITE_DB_NAME = "puchi_db.sqlite"
SQLITE_URL = f"sqlite:///./{SQLITE_DB_NAME}"

connect_args = {"check_same_thread": False}
engine = create_engine(SQLITE_URL, echo=True, connect_args=connect_args)


def init_db():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    engine.dispose()


def get_session():
    with Session(engine) as session:
        yield session
