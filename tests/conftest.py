import os
import tempfile

import pytest
from fastapi.testclient import TestClient

# Set the database path before importing the application.
_test_db = tempfile.NamedTemporaryFile(
    suffix=".db",
    delete=False,
)
_test_db.close()

os.environ["DATABASE_PATH"] = _test_db.name
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["GEMINI_API_KEY"] = ""

from app.main import app  # noqa: E402


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def registered_client(client):
    response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200
    return client