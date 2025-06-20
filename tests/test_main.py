from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

from api.db import create_db_and_tables, get_session
from main import app

# Create a test database (SQLite in-memory)
test_db_url = "sqlite:///./test.db"
test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create tables
create_db_and_tables(run_engine=test_engine)


# Dependency override
def override_get_session():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


def test_6_char_shorten_url(test_url_1):
    response = client.post("/", json=test_url_1)
    assert response.status_code == 201
    data = response.json()
    assert data["url"] == "https://example.com"
    assert data["shorten_url"] == "exampl"


def test_custom_shorten_url(test_url_2):
    response = client.post("/", json=test_url_2)
    assert response.status_code == 201
    data = response.json()
    assert data["url"] == "https://example123.com"
    assert data["shorten_url"] == "ex"


def test_root(test_url_1, test_url_2):
    client.post("/", json=test_url_1)
    client.post("/", json=test_url_2)
    response = client.get("/")
    assert response.status_code == 200
    test_data = [
        {
            "url": "https://example.com",
            "id": 1,
            "shorten_url": "exampl",
        },
        {"url": "https://example123.com", "id": 2, "shorten_url": "ex"},
    ]
    assert test_data == response.json()


def test_not_found():
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_conflict_url(test_url_1):
    # First request should succeed
    response = client.post("/", json=test_url_1)
    assert response.status_code == 201

    # Second request with the same URL should raise a conflict
    response = client.post("/", json=test_url_1)
    assert response.status_code == 409
    assert "URL already exists" in response.json()["detail"]


def test_conflict_shorten_url(test_url_2, test_url_3):
    # First request should succeed
    response = client.post("/", json=test_url_2)
    assert response.status_code == 201

    # Second request with the same shorten URL should raise a conflict
    response = client.post("/", json=test_url_3)
    assert response.status_code == 409
    assert (
        f"Short URL already exists: {test_url_3['shorten_url']}"
        in response.json()["detail"]
    )


def test_redirect(test_url_1):
    response = client.post("/", json=test_url_1)
    assert response.status_code == 201
    data = response.json()
    short_url = data["shorten_url"]

    response = client.get(f"/{short_url}", follow_redirects=False)
    assert response.status_code == 307  # Redirect status code
    assert (
        response.headers["Location"] == "https://example.com"
    )  # Check redirect location


def test_delete_url(test_url_1):
    response = client.post("/", json=test_url_1)
    assert response.status_code == 201
    data = response.json()
    short_url = data["shorten_url"]

    response = client.delete(f"/{short_url}")
    assert response.status_code == 200
    assert response.json() == {"detail": "URL deleted successfully"}

    # Verify the URL is deleted
    response = client.delete(f"/{short_url}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Short URL not found"}
