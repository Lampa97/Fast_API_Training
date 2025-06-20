from sqlmodel import Field, SQLModel


class URL(SQLModel, table=True):
    """Model for storing URLs in the database."""

    id: int = Field(default=None, primary_key=True)
    url: str = Field(index=True, max_length=256, unique=True)
    shorten_url: str | None = Field(default=None, max_length=6)
