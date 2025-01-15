from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from db.crud import add_click, get_link, get_links
from db.database import SessionDep, lifespan
from db.models import ErrorResponse
from core.puchi import api

app = FastAPI(lifespan=lifespan)
app.include_router(api)


@app.get("/links", responses={
    200:{ "description": "All links", "model": list[dict] }
})
def all_links(session: SessionDep):
    return get_links(session)


@app.get("/{short_url}", status_code=303, responses={
    303: {"description": "Redirecting..."},
    404: {"description": "Link not found", "model": ErrorResponse}
})
def redirect(short_url: str, session: SessionDep):
    if link := get_link(short_url, session):
        add_click(link, session)
        return RedirectResponse(f"{link.long_url}", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Link not found") 
