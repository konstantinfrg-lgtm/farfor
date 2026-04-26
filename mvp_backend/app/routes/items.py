from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Item, ItemPhoto, User
from app.db.session import get_db
from app.routes.deps import current_user
from app.schemas.items import ItemCreate, ItemOut, ItemUpdate, UserCollectionOut
from app.services.storage import upload_photo

router = APIRouter(prefix='/items', tags=['items'])


@router.post('/upload')
def upload_item_photo(file: UploadFile = File(...), _: User = Depends(current_user)):
    return {'url': upload_photo(file)}


@router.post('', response_model=ItemOut)
def create_item(payload: ItemCreate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = Item(owner_id=user.id, **payload.model_dump(exclude={'photo_urls'}))
    db.add(item)
    db.flush()

    for url in payload.photo_urls:
        db.add(ItemPhoto(item_id=item.id, url=url))

    db.commit()
    db.refresh(item)
    return item


@router.get('/me', response_model=list[ItemOut])
def list_my_items(
    q: str | None = None,
    material: str | None = None,
    period: str | None = None,
    is_public: bool | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    stmt = select(Item).where(Item.owner_id == user.id).options(selectinload(Item.photos)).order_by(Item.created_at.desc())
    filters = []
    if q:
        pattern = f'%{q}%'
        filters.append(or_(Item.title.ilike(pattern), Item.manufacturer.ilike(pattern), Item.comment.ilike(pattern)))
    if material:
        filters.append(Item.material.ilike(f'%{material}%'))
    if period:
        filters.append(Item.period.ilike(f'%{period}%'))
    if is_public is not None:
        filters.append(Item.is_public == is_public)
    if filters:
        stmt = stmt.where(and_(*filters))
    return list(db.scalars(stmt))


@router.get('/public', response_model=list[ItemOut])
def list_public_items(
    q: str | None = None,
    manufacturer: str | None = None,
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(Item).where(Item.is_public.is_(True)).options(selectinload(Item.photos)).order_by(Item.created_at.desc()).limit(limit)
    if q:
        stmt = stmt.where(or_(Item.title.ilike(f'%{q}%'), Item.comment.ilike(f'%{q}%')))
    if manufacturer:
        stmt = stmt.where(Item.manufacturer.ilike(f'%{manufacturer}%'))
    return list(db.scalars(stmt))


@router.put('/{item_id}', response_model=ItemOut)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = db.get(Item, item_id)
    if not item or item.owner_id != user.id:
        raise HTTPException(status_code=404, detail='Предмет не найден')

    for field, value in payload.model_dump(exclude_unset=True, exclude={'photo_urls'}).items():
        setattr(item, field, value)

    if payload.photo_urls is not None:
        item.photos.clear()
        for url in payload.photo_urls:
            item.photos.append(ItemPhoto(url=url))

    db.commit()
    db.refresh(item)
    return item


@router.delete('/{item_id}')
def delete_item(item_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = db.get(Item, item_id)
    if not item or item.owner_id != user.id:
        raise HTTPException(status_code=404, detail='Предмет не найден')
    db.delete(item)
    db.commit()
    return {'status': 'ok'}


@router.get('/collections/{username}', response_model=UserCollectionOut)
def public_collection(username: str, db: Session = Depends(get_db)):
    owner = db.scalar(select(User).where(User.username == username))
    if not owner:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    if owner.is_collection_public:
        items_stmt = select(Item).where(Item.owner_id == owner.id).options(selectinload(Item.photos)).order_by(Item.created_at.desc())
    else:
        items_stmt = select(Item).where(Item.owner_id == owner.id, Item.is_public.is_(True)).options(selectinload(Item.photos)).order_by(Item.created_at.desc())

    return UserCollectionOut(
        id=owner.id,
        username=owner.username,
        is_collection_public=owner.is_collection_public,
        items=list(db.scalars(items_stmt)),
    )


@router.patch('/me/collection-visibility', response_model=dict)
def set_collection_visibility(
    is_public: bool,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    user.is_collection_public = is_public
    db.commit()
    return {'is_collection_public': user.is_collection_public}
