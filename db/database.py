import json
from contextlib import asynccontextmanager
from typing import Annotated
from os import getenv

from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

    
SQLITE_DB_NAME = "puchi_db.sqlite"
SQLITE_URL = f"sqlite:///./{SQLITE_DB_NAME}"

class Wordbook(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Wordbook, cls).__new__(cls)
        return cls.instance

    def init_wb(self):
        try:
            with open("dict.json") as file:
                self.wordbook: dict[str, list[str]] = json.load(file)

                self.wordbook_PoS = tuple(self.wordbook.keys())
                self.wordbook_lens = tuple(map(len, self.wordbook.values()))
        except FileNotFoundError:
            print("JSON-файл не найден!")
        except json.JSONDecodeError:
            print("Ошибка в чтении файла!")



def _init_db():
    global engine
    connect_args = {"check_same_thread": False}
    engine = create_engine(SQLITE_URL, echo=True, connect_args=connect_args)
    SQLModel.metadata.create_all(engine)
    return engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    _init_db()
    Wordbook().init_wb()
    yield
    engine.dispose()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
