from enum import Enum

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class TypeEnum(str, Enum):
    humanlike = "humanlike"
    short = "short"
    other = "other"


class Link(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_id: int = Field(unique=True)
    short_url: str | None = Field(default=None, index=True)
    long_url: str
    clicks: int = Field(default=0)


class LongLink(BaseModel):
    url: str
    encoding_type: TypeEnum


class ShortLink(BaseModel):
    short_url: str
