import click
from flask.cli import with_appcontext

from app import create_app
from app.extensions import db
from app.models import Artist, Item, Manufacturer, PaintingStyle, Sculptor, Shape, User

app = create_app()


@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo("Database initialized.")


@click.command("seed-db")
@with_appcontext
def seed_db_command():
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
        item = Item(
            title="Молочник ЛФЗ",
            period="1950-е",
            material="Фарфор",
            comments="Демо-запись",
            publication_status="published",
            visibility="public",
            owner_id=owner.id,
        )
        db.session.add(item)
        db.session.commit()

    click.echo("Database seeded.")


app.cli.add_command(init_db_command)
app.cli.add_command(seed_db_command)
