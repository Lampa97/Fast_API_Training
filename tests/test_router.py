import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_catfact_route():
    response = client.get("/external/catfact")
    assert response.status_code == 200
    assert "fact" in response.json()