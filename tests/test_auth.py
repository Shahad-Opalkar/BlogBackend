def test_register(client):
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "123456"
    })

    assert response.status_code == 201
    assert response.json["email"] == "test@example.com"


def test_login_success(client):
    # Register first
    client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "123456"
    })

    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "123456"
    })

    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_invalid_credentials(client):
    response = client.post("/login", json={
        "email": "wrong@example.com",
        "password": "wrong"
    })

    assert response.status_code == 401

