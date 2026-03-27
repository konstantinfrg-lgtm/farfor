from __future__ import annotations

from sqlalchemy import asc, desc, or_

from ..models import Item, PublicationStatus, Visibility


SORT_MAP = {
    "newest": Item.created_at.desc(),
    "oldest": Item.created_at.asc(),
    "title_asc": asc(Item.title),
    "title_desc": desc(Item.title),
    "updated": Item.updated_at.desc(),
}


def build_catalog_query(current_user, args):
    query = Item.query

    if not (current_user.is_authenticated and current_user.is_admin):
        query = query.filter(Item.publication_status == PublicationStatus.PUBLISHED)
        if current_user.is_authenticated:
            query = query.filter(or_(Item.visibility == Visibility.PUBLIC, Item.owner_id == current_user.id))
        else:
            query = query.filter(Item.visibility == Visibility.PUBLIC)

    search = args.get("q", "").strip()
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(Item.title.ilike(pattern), Item.comments.ilike(pattern), Item.material.ilike(pattern)))

    for key in ["manufacturer_id", "artist_id", "shape_id", "painting_style_id", "owner_id"]:
        value = args.get(key, type=int)
        if value:
            query = query.filter(getattr(Item, key) == value)

    period = args.get("period", "").strip()
    if period:
        query = query.filter(Item.period.ilike(f"%{period}%"))

    sort = args.get("sort", "newest")
    order_by = SORT_MAP.get(sort, SORT_MAP["newest"])
    query = query.order_by(order_by)

    return query
