from fastapi import APIRouter
from fastapi.responses import JSONResponse


from db.crud import create_new, delete_link, get_max_id
from db.database import SessionDep
from db.models import Link, LongLink, ShortLink
from utils.generator import generate_phrase_url


api = APIRouter(prefix="/api", tags=["api"])


@api.post("/new_link", response_model=Link)
def new_url(request: LongLink, session: SessionDep):
    return create_new(Link(short_url=generate_phrase_url(get_max_id(session) + 1), long_url=request.url), session)


@api.delete("/delete_link")
def delete_short(request: ShortLink, session: SessionDep):
    if delete_link(request.short_url, session):
        return JSONResponse({"deleted": True, "link": request.short_url}, status_code=200)
    return JSONResponse({"deleted": False, "link": request.short_url}, status_code=403)
