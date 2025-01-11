from sqlmodel import Session, func, select

from db.models import Link


def create_new(link: Link, session: Session) -> Link:
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def get_links(session: Session):
    links = session.exec(select(Link)).all()
    return links


def get_link(short: str, session: Session) -> Link | None:
    link = session.exec(select(Link).where(Link.short_url == short)).first()
    if link:
        return link
    return None


def get_ids(session: Session):
    return session.exec(select(Link.id)).all()


def get_max_id(session: Session):
    if (max_id := session.exec(select(func.max(Link.id))).one()) is None: 
        return 0
    return  max_id


def delete_link(short: str, session: Session):
    link = session.exec(select(Link).where(Link.short_url == short)).first()
    if link:
        session.delete(link)
        session.commit()
        return link
    return None


def add_click(link: Link, session: Session):
    link.clicks += 1
    session.add(link)
    session.commit()
    session.refresh(link)
    return link
