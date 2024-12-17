from sqlmodel import Field, SQLModel


class Link(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_url: str | None = Field(default=None, index=True)
    short_id: int = Field(unique=True)
    long_url: str
    clicks: int = Field(default=0)
