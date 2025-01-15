from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse


from db.crud import create_new, delete_link, get_max_id
from db.database import SessionDep
from db.models import ErrorResponse, Link, NewLink, ShortLink
from .generator import generate_phrase_url


api = APIRouter(prefix="/api", tags=["api"])


@api.post("/new_link", response_model=Link, responses={
    200: {"description": "Link created successfully", "model": Link},
    400: {"description": "Bad Request", "model": ErrorResponse}
})
def new_url(request: NewLink, session: SessionDep):
    try:
        return create_new(Link(short_url=generate_phrase_url(get_max_id(session) + 1), long_url=request.url), session)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.delete("/delete_link", responses={
    200: {"description": "Link deleted", "model": Link},
    404: {"description": "Link not found", "model": ErrorResponse}  
})
def delete_short(request: ShortLink, session: SessionDep):
    if delete_link(request.short_url, session):
        return JSONResponse({"deleted": True, "link": request.short_url}, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Link not found")
