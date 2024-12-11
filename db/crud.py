from sqlmodel import Session, select

from db.models import Link


def create_new_short(link: Link, session: Session) -> Link:
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def get_links(session: Session):
    links = session.exec(select(Link))
    return links


def get_link(short: str, session: Session) -> Link | None:
    link = session.exec(select(Link).where(Link.short_url == short)).first()
    if link:
        return link
    return None


def increment_click(link: Link, session: Session):
    link.clicks += 1
    session.add(link)
    session.commit()
    session.refresh(link)
    return link
