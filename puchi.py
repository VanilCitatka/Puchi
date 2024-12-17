import random

from fastapi import APIRouter

from db.crud import create_new
from db.database import SessionDep, URL_Words
from db.models import Link


# TODO: Хуйня, переделать
def generate_short_url(id: int) -> str:
    words = URL_Words()
    adj = words.adjs[id % 128].capitalize()
    noun = words.nouns[id // 128 % 128].capitalize()
    vrb = words.vrbs[id // 128 // 128 % 128].capitalize()
    advrb = words.advrbs[id // 128 // 128 // 128 % 128].capitalize()
    return "".join((adj, noun, vrb, advrb))


api = APIRouter(prefix="/api", tags=["api"])


@api.post("/new_url")
def new_url(request: Link, session: SessionDep):
    id = random.choice(range(0, 1000))
    short = generate_short_url(id)
    return create_new(
        Link(short_url=short, short_id=id, long_url=request.long_url), session
    )
