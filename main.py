from typing import Annotated, Sequence
from urllib.parse import urlparse
from api.router import router
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from api.models import URL
from api.db import create_db_and_tables, get_session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


app.include_router(router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/", status_code=status.HTTP_201_CREATED)
def shorten_url(url: URL, session: SessionDep) -> URL:
    existing = session.exec(select(URL).where(URL.url == url.url)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"URL already exists. Short URL: {existing.shorten_url}",
        )
    full_url = url.url
    domain_url = urlparse(full_url).netloc  # Get the domain part
    short_url = domain_url.split(".")[0][
        :6
    ]  # Take the first 6 characters of the domain

    # If the user passed a short URL, use it; otherwise, assign the generated one
    url.shorten_url = url.shorten_url or short_url

    session.add(url)
    session.commit()
    session.refresh(url)
    return url


@app.get("/")
def read_urls(session: SessionDep) -> Sequence[URL]:
    urls = session.exec(select(URL)).all()
    return urls


@app.get("/{shorten_url}")
async def get_original_url(shorten_url: str, session: SessionDep) -> RedirectResponse:
    original_url = session.exec(
        select(URL).where(URL.shorten_url == shorten_url)
    ).first()
    if not original_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=original_url.url, status_code=307)

