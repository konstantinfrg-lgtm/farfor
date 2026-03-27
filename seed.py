from app import create_app
from app.extensions import db
from app.models import Artist, Item, Manufacturer, PaintingStyle, Sculptor, Shape, User

app = create_app("development")

with app.app_context():
    db.create_all()

    if not User.query.filter_by(email="admin@example.com").first():
        admin = User(username="admin", email="admin@example.com", full_name="Admin", is_admin=True)
        admin.set_password("admin12345")
        user = User(username="collector", email="collector@example.com", full_name="Collector")
        user.set_password("collector12345")
        db.session.add_all([admin, user])

    for model, values in [
        (Manufacturer, ["ЛФЗ", "Дулёво"]),
        (Sculptor, ["Иванов"]),
        (Artist, ["Петров"]),
        (Shape, ["Классическая"]),
        (PaintingStyle, ["Кобальтовая сетка"]),
    ]:
        for value in values:
            if not model.query.filter_by(name=value).first():
                db.session.add(model(name=value))

    db.session.commit()

    if not Item.query.first():
        owner = User.query.filter_by(username="collector").first()
        item = Item(title="Молочник ЛФЗ", period="1950-е", material="Фарфор", comments="Демо-запись", publication_status="published", visibility="public", owner_id=owner.id)
        db.session.add(item)
        db.session.commit()

    print("Seed completed")
