from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    manufacturer: str = Field(min_length=2, max_length=180)
    shape_author: str | None = None
    painting_author: str | None = None
    shape_name: str | None = None
    painting_name: str | None = None
    production_year: int | None = None
    period: str | None = None
    material: str | None = None
    condition: str | None = None
    size: str | None = None
    location: str | None = None
    comment: str | None = None
    is_public: bool = False


class ItemCreate(ItemBase):
    photo_urls: list[str] = []


class ItemUpdate(BaseModel):
    title: str | None = None
    manufacturer: str | None = None
    shape_author: str | None = None
    painting_author: str | None = None
    shape_name: str | None = None
    painting_name: str | None = None
    production_year: int | None = None
    period: str | None = None
    material: str | None = None
    condition: str | None = None
    size: str | None = None
    location: str | None = None
    comment: str | None = None
    is_public: bool | None = None
    photo_urls: list[str] | None = None


class ItemPhotoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    url: str


class ItemOut(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    photos: list[ItemPhotoOut] = []


class UserCollectionOut(BaseModel):
    id: int
    username: str
    is_collection_public: bool
    items: list[ItemOut]
