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


@app.post("/")
def shorten_url(link: Link, session: SessionDep) -> Link:
    # Simple shortening logic - first 6 characters before the dot
    link.shorten_url = link.shorten_url or link.url[:6].split('.', 1)[0]
    session.add(link)
    session.commit()
    session.refresh(link)
    return link

@app.get("/links/")
def read_links(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Link]:
    links = session.exec(select(Link).offset(offset).limit(limit)).all()
    return links

@app.get("/{shorten_url}")
async def get_original_url(shorten_url: str, session: SessionDep) -> Link:
    original_url = session.get(Link, shorten_url)
    if not original_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return original_url
