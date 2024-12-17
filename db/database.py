import json
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

SQLITE_DB_NAME = "puchi_db.sqlite"
SQLITE_URL = f"sqlite:///./{SQLITE_DB_NAME}"

connect_args = {"check_same_thread": False}
engine = create_engine(SQLITE_URL, echo=True, connect_args=connect_args)


class URL_Words(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(URL_Words, cls).__new__(cls)
        return cls.instance

    def init_dict(self):
        try:
            with open("dict.json") as file:
                data = json.load(file)

                self.adjs: list[str] = data.get("Adjectives", [])
                self.nouns: list[str] = data.get("Nouns", [])
                self.vrbs: list[str] = data.get("Verbs", [])
                self.advrbs: list[str] = data.get("Adverbs", [])

                self.dict_len = 128
        except FileNotFoundError:
            print("JSON-файл не найден!")
        except json.JSONDecodeError:
            print("Ошибка в чтении файла!")

    def get_words(self):
        return self.adjs, self.nouns, self.vrbs, self.advrbs


def _init_db():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _init_db()
    URL_Words().init_dict()
    yield
    engine.dispose()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
