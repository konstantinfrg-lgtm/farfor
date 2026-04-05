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


def test_registered_visibility_only_for_authenticated(client, app):
    with app.app_context():
        user = User.query.filter_by(username="user").first()
        db.session.add(
            Item(title="Только для зарегистрированных", owner_id=user.id, publication_status="published", visibility="registered")
        )
        db.session.commit()

    guest_response = client.get("/catalog?mode=all")
    assert "Только для зарегистрированных" not in guest_response.get_data(as_text=True)

    login(client)
    auth_response = client.get("/catalog?mode=all")
    assert "Только для зарегистрированных" in auth_response.get_data(as_text=True)


def test_my_collection_mode_shows_only_current_user_items(client, app):
    with app.app_context():
        user = User.query.filter_by(username="user").first()
        admin = User.query.filter_by(username="admin").first()
        db.session.add(Item(title="Предмет пользователя", owner_id=user.id, publication_status="draft", visibility="private"))
        db.session.add(Item(title="Предмет админа", owner_id=admin.id, publication_status="published", visibility="public"))
        db.session.commit()

    login(client, "user@test.local")
    response = client.get("/catalog?mode=my")
    body = response.get_data(as_text=True)
    assert "Предмет пользователя" in body
    assert "Предмет админа" not in body
