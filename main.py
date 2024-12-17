from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

from db.crud import add_click, get_link, get_links
from db.database import SessionDep, lifespan
from puchi import api

app = FastAPI(lifespan=lifespan)
app.include_router(api)


# TODO: Route to REACT Main page
@app.get("/")
def index():
    return HTMLResponse("<h1>Hello World!</h1>")


@app.get("/links")
def all_links(session: SessionDep):
    return get_links(session)


@app.get("/{short_url}")
def redirect(short_url: str, session: SessionDep):
    if link := get_link(short_url, session):
        add_click(link, session)
        return RedirectResponse(f"{link.long_url}", status_code=303)
    return HTMLResponse("""
                            <h1>Хуйня. Не найдено</h1>
                        """)
