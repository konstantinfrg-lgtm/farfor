import pytest

from app import create_app
from app.extensions import db
from app.models import User


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        admin = User(username="admin", email="admin@test.local", is_admin=True)
        admin.set_password("password123")
        user = User(username="user", email="user@test.local")
        user.set_password("password123")
        db.session.add_all([admin, user])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
