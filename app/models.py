from __future__ import annotations

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Visibility:
    PUBLIC = "public"
    PRIVATE = "private"


class PublicationStatus:
    DRAFT = "draft"
    PUBLISHED = "published"


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))
    bio = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    items = db.relationship("Item", back_populates="owner", lazy="dynamic", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))


class LookupBase(TimestampMixin, db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)


class Manufacturer(LookupBase):
    __tablename__ = "manufacturers"


class Sculptor(LookupBase):
    __tablename__ = "sculptors"


class Artist(LookupBase):
    __tablename__ = "artists"


class Shape(LookupBase):
    __tablename__ = "shapes"


class PaintingStyle(LookupBase):
    __tablename__ = "painting_styles"


class Item(TimestampMixin, db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    period = db.Column(db.String(120), index=True)
    material = db.Column(db.String(120))
    comments = db.Column(db.Text)
    publication_status = db.Column(db.String(20), default=PublicationStatus.DRAFT, nullable=False, index=True)
    visibility = db.Column(db.String(20), default=Visibility.PUBLIC, nullable=False, index=True)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey("manufacturers.id"), index=True)
    sculptor_id = db.Column(db.Integer, db.ForeignKey("sculptors.id"), index=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), index=True)
    shape_id = db.Column(db.Integer, db.ForeignKey("shapes.id"), index=True)
    painting_style_id = db.Column(db.Integer, db.ForeignKey("painting_styles.id"), index=True)

    owner = db.relationship("User", back_populates="items")
    manufacturer = db.relationship("Manufacturer")
    sculptor = db.relationship("Sculptor")
    artist = db.relationship("Artist")
    shape = db.relationship("Shape")
    painting_style = db.relationship("PaintingStyle")
    photos = db.relationship("Photo", back_populates="item", cascade="all, delete-orphan", lazy="selectin")


class Photo(TimestampMixin, db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255))

    item = db.relationship("Item", back_populates="photos")
