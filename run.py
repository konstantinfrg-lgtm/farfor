import os

from app import create_app
from app.extensions import db
from app.models import Artist, Item, Manufacturer, PaintingStyle, Photo, Sculptor, Shape, User

config_name = os.getenv("FLASK_ENV", "development")
app = create_app(config_name)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Item": Item,
        "Photo": Photo,
        "Manufacturer": Manufacturer,
        "Sculptor": Sculptor,
        "Artist": Artist,
        "Shape": Shape,
        "PaintingStyle": PaintingStyle,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
