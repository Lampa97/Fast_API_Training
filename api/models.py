from sqlmodel import Field, SQLModel

class URL(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str = Field(index=True, max_length=256, unique=True)
    shorten_url: str | None = Field(default=None, max_length=6)