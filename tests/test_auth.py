def test_register_and_login(client):
    response = client.post(
        "/auth/register",
        data={
            "username": "newuser",
            "email": "new@test.local",
            "password": "password123",
            "password2": "password123",
        },
        follow_redirects=True,
    )
    assert "Регистрация успешно завершена" in response.get_data(as_text=True)

    response = client.post(
        "/auth/login",
        data={"email": "new@test.local", "password": "password123"},
        follow_redirects=True,
    )
    assert "Вы успешно вошли" in response.get_data(as_text=True)
