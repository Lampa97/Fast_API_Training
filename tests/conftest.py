import pytest
from sqlmodel import SQLModel

from tests.test_main import test_engine


@pytest.fixture(autouse=True)
def clean_db():
    SQLModel.metadata.drop_all(bind=test_engine)
    SQLModel.metadata.create_all(bind=test_engine)
    yield


@pytest.fixture
def test_url_1():
    """Fixture for a test URL."""
    return {
        "url": "https://example.com",
    }


@pytest.fixture
def test_url_2():
    """Fixture for another test URL."""
    return {"url": "https://example123.com", "shorten_url": "ex"}


@pytest.fixture
def test_url_3():
    """Fixture for another test URL."""
    return {"url": "https://example1.com", "shorten_url": "ex"}
