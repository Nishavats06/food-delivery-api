def test_register_success(client):
    response = client.post("/auth/register", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone_number": "9876543210",
        "password": "test123",
        "role": "CUSTOMER",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "duplicate@example.com",
        "phone_number": "9876543210",
        "password": "test123",
        "role": "CUSTOMER",
    }
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400


def test_register_weak_password(client):
    response = client.post("/auth/register", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "weak@example.com",
        "phone_number": "9876543210",
        "password": "123",
        "role": "CUSTOMER",
    })
    assert response.status_code == 422


def test_login_success(client):
    client.post("/auth/register", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "login@example.com",
        "phone_number": "9876543210",
        "password": "test123",
        "role": "CUSTOMER",
    })
    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "test123",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "wrongpass@example.com",
        "phone_number": "9876543210",
        "password": "test123",
        "role": "CUSTOMER",
    })
    response = client.post("/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "incorrect",
    })
    assert response.status_code == 401


def test_me_requires_auth(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_with_valid_token(client):
    client.post("/auth/register", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "me@example.com",
        "phone_number": "9876543210",
        "password": "test123",
        "role": "CUSTOMER",
    })
    login_response = client.post("/auth/login", json={
        "email": "me@example.com",
        "password": "test123",
    })
    token = login_response.json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"