import pytest
import os
import tempfile
import uuid

import pytest
from fastapi.testclient import TestClient

# Create a separate test database.
_test_db = tempfile.NamedTemporaryFile(
    suffix=".db",
    delete=False,
)
_test_db.close()

os.environ["DATABASE_PATH"] = _test_db.name
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["GEMINI_API_KEY"] = ""

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def registered_client(client):
    email = f"test_{uuid.uuid4().hex}@example.com"

    response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200, response.text

    return client

