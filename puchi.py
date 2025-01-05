import random

from fastapi import APIRouter

from db.crud import create_new, delete_link, get_ids
from db.database import SessionDep, URL_Words
from db.models import Link, LongLink, ShortLink


# TODO: Хуйня, переделать
def generate_phrase_url(id: int) -> str:
    words = URL_Words()
    idx = []
    while id:
        idx.append(id % 512)
        id //= 512
    if len(idx) < 4:
        idx += [0] * (4 - len(idx))
    elif len(idx) < 4:
        raise ValueError("Too big id")

    adjs = words.adjs[idx[0]].capitalize()
    nouns = words.nouns[idx[1]].capitalize()
    vrbs = words.vrbs[idx[2]].capitalize()
    advrbs = words.advrbs[idx[3]].capitalize()

    return f"{adjs}{nouns}{vrbs}{advrbs}"


api = APIRouter(prefix="/api", tags=["api"])


@api.post("/new", response_model=Link)
def new_url(request: LongLink, session: SessionDep):
    while (id := random.randint(0, 128 ^ 4)) in set(get_ids(session)):
        continue
    short = generate_phrase_url(id)
    return create_new(Link(short_url=short, short_id=id, long_url=request.url), session)


@api.delete("/delete_short")
def delete_short(request: ShortLink, session: SessionDep):
    if link := delete_link(request.short_url, session):
        return {"deleted": True, "link": link}
    return {"deleted": False, "reason": "Я ебу? Ну не найдено наверное, я хз"}
