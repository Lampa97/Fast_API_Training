from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Link(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str = Field(index=True, max_length=256)
    shorten_url: str | None = Field(default=None, max_length=6)

sqlite_file_name = "links.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


