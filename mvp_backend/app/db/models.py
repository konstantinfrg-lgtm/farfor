from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_collection_public: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    items: Mapped[list['Item']] = relationship('Item', back_populates='owner', cascade='all, delete-orphan')


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(180), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(180), nullable=False)
    shape_author: Mapped[str | None] = mapped_column(String(180))
    painting_author: Mapped[str | None] = mapped_column(String(180))
    shape_name: Mapped[str | None] = mapped_column(String(180))
    painting_name: Mapped[str | None] = mapped_column(String(180))
    production_year: Mapped[int | None] = mapped_column(Integer)
    period: Mapped[str | None] = mapped_column(String(120))
    material: Mapped[str | None] = mapped_column(String(120))
    condition: Mapped[str | None] = mapped_column(String(120))
    size: Mapped[str | None] = mapped_column(String(120))
    location: Mapped[str | None] = mapped_column(String(180))
    comment: Mapped[str | None] = mapped_column(Text)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner: Mapped[User] = relationship('User', back_populates='items')
    photos: Mapped[list['ItemPhoto']] = relationship('ItemPhoto', back_populates='item', cascade='all, delete-orphan')


class ItemPhoto(Base):
    __tablename__ = 'item_photos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False, index=True)
    url: Mapped[str] = mapped_column(String(500), nullable=False)

    item: Mapped[Item] = relationship('Item', back_populates='photos')
