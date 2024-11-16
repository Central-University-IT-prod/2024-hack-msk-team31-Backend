from . import client


def test_register_user():
    register_data = {
        "login": "register_user",
        "password": "password123",
        "name": "Test User",
    }

    response = client.post("/user/register", json=register_data)

    assert response.status_code == 200
    assert "accessToken" in response.json()


def test_register_user_conflict():
    register_data = {
        "login": "user_conflict",
        "password": "password123",
        "name": "Test User",
    }
    resp = client.post("/user/register", json=register_data)
    assert resp.status_code == 200

    resp = client.post("/user/register", json=register_data)
    assert resp.status_code == 409


def test_login_user():
    register_data = {
        "login": "login_user",
        "password": "password123",
        "name": "Test User",
    }

    resp = client.post("/user/register", json=register_data)
    assert resp.status_code == 200

    login_data = {"login": "login_user", "password": "password123"}
    resp = client.post("/user/login", json=login_data)
    assert resp.status_code == 200
    assert "accessToken" in resp.json()

    login_data = {"login": "login_user", "password": "password1234"}
    resp = client.post("/user/login", json=login_data)
    assert resp.status_code == 401


def test_get_me():
    register_data = {
        "login": "get_me",
        "password": "password123",
        "name": "Test User",
    }

    resp = client.post("/user/register", json=register_data)
    assert resp.status_code == 200

    login_data = {"login": "get_me", "password": "password123"}

    login_resp = client.post("/user/login", json=login_data)
    assert login_resp.status_code == 200
    access_token = login_resp.json()["accessToken"]

    response = client.get(
        "/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["id"] > 0
    assert resp_data["login"] == "get_me"
    assert resp_data["name"] == "Test User"
