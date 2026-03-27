from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..forms import ItemForm, UploadPhotoForm
from ..models import Artist, Item, Manufacturer, PaintingStyle, Photo, Sculptor, Shape
from ..services.file_service import remove_image, save_image

items_bp = Blueprint("items", __name__)


def _setup_lookup_choices(form):
    empty = [(0, "—")]
    form.manufacturer_id.choices = empty + [(x.id, x.name) for x in Manufacturer.query.order_by(Manufacturer.name).all()]
    form.sculptor_id.choices = empty + [(x.id, x.name) for x in Sculptor.query.order_by(Sculptor.name).all()]
    form.artist_id.choices = empty + [(x.id, x.name) for x in Artist.query.order_by(Artist.name).all()]
    form.shape_id.choices = empty + [(x.id, x.name) for x in Shape.query.order_by(Shape.name).all()]
    form.painting_style_id.choices = empty + [(x.id, x.name) for x in PaintingStyle.query.order_by(PaintingStyle.name).all()]


def _can_edit(item: Item) -> bool:
    return current_user.is_authenticated and (current_user.is_admin or item.owner_id == current_user.id)


@items_bp.route("/<int:item_id>")
def detail(item_id):
    item = Item.query.get_or_404(item_id)
    if not _can_edit(item):
        if item.visibility != "public" or item.publication_status != "published":
            return render_template("errors/403.html"), 403
    return render_template("items/detail.html", item=item)


@items_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = ItemForm()
    _setup_lookup_choices(form)

    if form.validate_on_submit():
        item = Item(
            title=form.title.data,
            period=form.period.data,
            material=form.material.data,
            comments=form.comments.data,
            publication_status=form.publication_status.data,
            visibility=form.visibility.data,
            owner_id=current_user.id,
            manufacturer_id=form.manufacturer_id.data or None,
            sculptor_id=form.sculptor_id.data or None,
            artist_id=form.artist_id.data or None,
            shape_id=form.shape_id.data or None,
            painting_style_id=form.painting_style_id.data or None,
        )
        db.session.add(item)
        db.session.commit()
        flash("Карточка создана.", "success")
        return redirect(url_for("items.edit", item_id=item.id))
    return render_template("items/form.html", form=form, title="Создание карточки")


@items_bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit(item_id):
    item = Item.query.get_or_404(item_id)
    if not _can_edit(item):
        return render_template("errors/403.html"), 403

    form = ItemForm(obj=item)
    _setup_lookup_choices(form)

    if form.validate_on_submit():
        form.populate_obj(item)
        item.manufacturer_id = form.manufacturer_id.data or None
        item.sculptor_id = form.sculptor_id.data or None
        item.artist_id = form.artist_id.data or None
        item.shape_id = form.shape_id.data or None
        item.painting_style_id = form.painting_style_id.data or None
        db.session.commit()
        flash("Карточка обновлена.", "success")
        return redirect(url_for("items.detail", item_id=item.id))

    photo_form = UploadPhotoForm()
    return render_template("items/form.html", form=form, photo_form=photo_form, item=item, title="Редактирование карточки")


@items_bp.route("/<int:item_id>/delete", methods=["POST"])
@login_required
def delete(item_id):
    item = Item.query.get_or_404(item_id)
    if not _can_edit(item):
        return render_template("errors/403.html"), 403

    for photo in item.photos:
        remove_image(photo.filename)
    db.session.delete(item)
    db.session.commit()
    flash("Карточка удалена.", "info")
    return redirect(url_for("main.catalog"))


@items_bp.route("/<int:item_id>/photos", methods=["POST"])
@login_required
def upload_photos(item_id):
    item = Item.query.get_or_404(item_id)
    if not _can_edit(item):
        return render_template("errors/403.html"), 403

    form = UploadPhotoForm()
    if not form.validate_on_submit():
        flash("Не удалось загрузить фото: проверьте формат файла.", "danger")
        return redirect(url_for("items.edit", item_id=item_id))

    files = request.files.getlist("photos")
    if not files:
        flash("Не выбраны файлы.", "warning")
        return redirect(url_for("items.edit", item_id=item_id))

    uploaded = 0
    for file in files:
        try:
            filename = save_image(file)
        except Exception:
            continue
        db.session.add(Photo(item_id=item.id, filename=filename, original_name=file.filename))
        uploaded += 1

    db.session.commit()
    flash(f"Загружено файлов: {uploaded}", "success" if uploaded else "warning")
    return redirect(url_for("items.edit", item_id=item_id))


@items_bp.route("/photos/<int:photo_id>/delete", methods=["POST"])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if not _can_edit(photo.item):
        return render_template("errors/403.html"), 403

    item_id = photo.item_id
    remove_image(photo.filename)
    db.session.delete(photo)
    db.session.commit()
    flash("Фото удалено.", "info")
    return redirect(url_for("items.edit", item_id=item_id))
