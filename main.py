from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session

from db.crud import get_link, get_links
from db.database import get_session, lifespan
from puchi import puchi

app = FastAPI(lifespan=lifespan)
app.include_router(puchi)


# TODO: Route to REACT Main page
@app.get("/")
def index():
    return HTMLResponse("<h1>Hello World!</h1>")


@app.get("/links")
def all_links(session: Session = Depends(get_session)):
    return get_links(session)


@app.get("/{short_url}")
def redirect(short_url: str, session: Session = Depends(get_session)):
    if link := get_link(short_url, session):
        return RedirectResponse(f"{link.long_url}", status_code=303)
    return HTMLResponse("""
                            <h1>Хуйня. Не найдено</h1>
                        """)
