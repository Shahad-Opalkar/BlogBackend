def test_create_post_requires_auth(client):
    response = client.post("/posts", json={
        "title": "Test",
        "content": "Content"
    })

    assert response.status_code == 401


def test_create_post_success(client):
    # Register
    client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "123456"
    })

    # Login
    login = client.post("/login", json={
        "email": "test@example.com",
        "password": "123456"
    })

    token = login.json["access_token"]

    response = client.post(
        "/posts",
        json={"title": "Hello", "content": "World"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201


def test_update_post_forbidden(client):
    # Create user1
    client.post("/register", json={
        "username": "user1",
        "email": "user1@test.com",
        "password": "123456"
    })

    login1 = client.post("/login", json={
        "email": "user1@test.com",
        "password": "123456"
    })

    token1 = login1.json["access_token"]

    # Create post
    post = client.post(
        "/posts",
        json={"title": "Title", "content": "Content"},
        headers={"Authorization": f"Bearer {token1}"}
    )

    post_id = post.json["id"]

    # Create user2
    client.post("/register", json={
        "username": "user2",
        "email": "user2@test.com",
        "password": "123456"
    })

    login2 = client.post("/login", json={
        "email": "user2@test.com",
        "password": "123456"
    })

    token2 = login2.json["access_token"]

    # Try updating as user2
    response = client.put(
        f"/posts/{post_id}",
        json={"title": "Hacked"},
        headers={"Authorization": f"Bearer {token2}"}
    )

    assert response.status_code == 403