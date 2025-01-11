from pydantic import BaseModel
from sqlmodel import Field, SQLModel

#TODO: MAKE IT PRETTIER!!!

class Link(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_url: str | None 
    long_url: str
    clicks: int = Field(default=0)
    immutable: bool = Field(default=False)


class LongLink(BaseModel):
    url: str


class ShortLink(BaseModel):
    short_url: str
