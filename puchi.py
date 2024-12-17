import random

from fastapi import APIRouter
from sqids import Sqids  # type: ignore

from db.crud import create_new, delete_link, get_ids
from db.database import SessionDep, URL_Words
from db.models import Link, LongLink, ShortLink, TypeEnum


# TODO: Хуйня, переделать
def generate_short_url(id: int) -> str:
    words = URL_Words()
    adj = words.adjs[id % 128].capitalize()
    noun = words.nouns[id // 128 % 128].capitalize()
    vrb = words.vrbs[id // 128 // 128 % 128].capitalize()
    advrb = words.advrbs[id // 128 // 128 // 128 % 128].capitalize()
    return "".join((adj, noun, vrb, advrb))


api = APIRouter(prefix="/api", tags=["api"])


@api.post("/new", response_model=Link)
def new_url(request: LongLink, session: SessionDep):
    while (id := random.randint(0, 128 ^ 4)) in set(get_ids(session)):
        continue

    if request.encoding_type is TypeEnum.humanlike:
        short = generate_short_url(id)
    elif request.encoding_type is TypeEnum.short:
        sqids = Sqids(min_length=7)
        short = sqids.encode([id, 1488])  # МОДЕРАТОРЫ АУ ЗА КОМПЛИМЕНТЫ БАНЯТ
    return create_new(Link(short_url=short, short_id=id, long_url=request.url), session)


@api.delete("/delete_short")
def delete_short(request: ShortLink, session: SessionDep):
    if link := delete_link(request.short_url, session):
        return {"deleted": True, "link": link}
    return {"deleted": False, "reason": "Я ебу? Ну не найдено наверное, я хз"}
