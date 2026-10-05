def test_register_and_session(registered_client):
    response = registered_client.get("/session-info")

    assert response.status_code == 200

    email = response.json()["email"]

    assert email.startswith("test_")
    assert email.endswith("@example.com")