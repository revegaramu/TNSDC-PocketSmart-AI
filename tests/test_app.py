def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_and_session(registered_client):
    response = registered_client.get("/session-info")

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_duplicate_registration(client):
    payload = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "TestPassword123",
    }

    first = client.post("/register", json=payload)
    second = client.post("/register", json=payload)

    assert first.status_code == 200
    assert second.status_code == 409


def test_login(client):
    client.post(
        "/register",
        json={
            "name": "Login User",
            "email": "login@example.com",
            "password": "Password12345",
        },
    )

    client.post("/logout")

    response = client.post(
        "/login",
        json={
            "email": "login@example.com",
            "password": "Password12345",
        },
    )

    assert response.status_code == 200
    assert response.json()["redirect"] == "/dashboard"


def test_recommendation_requires_login(client):
    response = client.post(
        "/generate-home",
        json={
            "room_type": "Bedroom",
            "budget": 25000,
            "style": "Modern",
            "notes": "",
        },
    )

    assert response.status_code == 401


def test_home_recommendation(registered_client):
    response = registered_client.post(
        "/generate-home",
        json={
            "room_type": "Bedroom",
            "budget": 25000,
            "style": "Modern",
            "notes": "Prefer simple furniture",
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert result["id"] > 0
    assert result["items"]
    assert result["estimated_total"] <= 25000


def test_party_recommendation(registered_client):
    response = registered_client.post(
        "/generate-party",
        json={
            "occasion": "Birthday",
            "budget": 20000,
            "guests": 30,
            "location_type": "Indoor",
            "notes": "",
        },
    )

    assert response.status_code == 200
    assert response.json()["items"]


def test_jewelry_recommendation(registered_client):
    response = registered_client.post(
        "/generate-jewelry",
        json={
            "occasion": "Festival",
            "outfit_color": "Maroon",
            "budget": 5000,
            "jewelry_type": "Traditional",
            "notes": "",
        },
    )

    assert response.status_code == 200
    assert response.json()["items"]


def test_history(registered_client):
    registered_client.post(
        "/generate-home",
        json={
            "room_type": "Study room",
            "budget": 10000,
            "style": "Minimalist",
            "notes": "",
        },
    )

    response = registered_client.get("/history")

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_dashboard_redirects_when_logged_out(client):
    response = client.get(
        "/dashboard",
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/login"