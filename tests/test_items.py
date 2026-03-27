from app.extensions import db
from app.models import Item, User


def login(client, email="user@test.local", password="password123"):
    return client.post("/auth/login", data={"email": email, "password": password}, follow_redirects=True)


def test_create_item(client):
    login(client)
    response = client.post(
        "/items/create",
        data={"title": "Тестовый молочник", "publication_status": "published", "visibility": "public"},
        follow_redirects=True,
    )
    assert "Карточка создана" in response.get_data(as_text=True)


def test_catalog_view(client, app):
    with app.app_context():
        user = User.query.filter_by(username="user").first()
        db.session.add(Item(title="Публичный", owner_id=user.id, publication_status="published", visibility="public"))
        db.session.commit()

    response = client.get("/catalog")
    assert response.status_code == 200
    assert "Публичный" in response.get_data(as_text=True)
