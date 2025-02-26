from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse


from db.crud import create_link, delete_link, get_all, get_details, get_max_id
from db.database import SessionDep
from db.models import ErrorResponse, Link
from .generator import generate_phrase_url


api = APIRouter(prefix="/api", tags=["api"])

@api.get("/")
def get_all_links(session: SessionDep):
    return get_all(session)


@api.post("/", response_model=Link, responses={
    200: {"description": "Link created successfully", "model": Link},
    400: {"description": "Bad Request", "model": ErrorResponse}
})
def create_new_link(request: Link, session: SessionDep):
    try:
        if 'http://' not in request.long_url or 'https://' not in request.long_url:
            long_url = 'http://' + request.long_url
        else:
            long_url = request.long_url
        return create_link(Link(short_url=generate_phrase_url(get_max_id(session) + 1), long_url=long_url), session)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.get("/{short_link}")
def get_link_details(short_link: str, session: SessionDep):
    if details := get_details(short_link, session):
        return details
    raise HTTPException(status_code=404, detail="Not found")


@api.delete("/{short_link}", responses={
    200: {"description": "Link deleted", "model": Link},
    404: {"description": "Link not found", "model": ErrorResponse}  
})
def delete_short_link(short_link: str, session: SessionDep):
    if delete_link(short_link, session):
        return JSONResponse({"deleted": True, "link": short_link}, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Not found")
