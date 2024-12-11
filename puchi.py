from random import choices
from string import ascii_letters, digits

from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.crud import create_new_short
from db.database import get_session
from db.models import Link

FULL_ASCII = list(ascii_letters + digits)

puchi = APIRouter(prefix="/api")


def create_short_url():
    return "".join(choices(FULL_ASCII, k=6))


@puchi.post("/make_short")
def make_short(long: Link, session: Session = Depends(get_session)) -> Link:
    link = Link(short_url=create_short_url(), long_url=long.long_url)
    return create_new_short(link, session)
