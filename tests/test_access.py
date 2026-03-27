def login(client, email, password="password123"):
    return client.post("/auth/login", data={"email": email, "password": password}, follow_redirects=True)


def test_access_control_admin_routes(client):
    login(client, "user@test.local")
    response = client.get("/admin/", follow_redirects=False)
    assert response.status_code == 403


def test_admin_routes_for_admin(client):
    login(client, "admin@test.local")
    response = client.get("/admin/", follow_redirects=False)
    assert response.status_code == 200
