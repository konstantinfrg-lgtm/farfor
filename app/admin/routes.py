from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import LookupForm
from ..models import Artist, Item, Manufacturer, PaintingStyle, Sculptor, Shape, User
from ..utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__)

LOOKUP_MODELS = {
    "manufacturers": Manufacturer,
    "sculptors": Sculptor,
    "artists": Artist,
    "shapes": Shape,
    "painting_styles": PaintingStyle,
}


def _get_or_404(model, object_id: int):
    obj = db.session.get(model, object_id)
    if obj is None:
        abort(404)
    return obj


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    return render_template(
        "admin/dashboard.html",
        users_count=User.query.count(),
        items_count=Item.query.count(),
    )


@admin_bp.route("/users")
@login_required
@admin_required
def users():
    page = request.args.get("page", 1, type=int)
    pagination = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template("admin/users.html", pagination=pagination)


@admin_bp.route("/items")
@login_required
@admin_required
def items():
    page = request.args.get("page", 1, type=int)
    pagination = Item.query.order_by(Item.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template("admin/items.html", pagination=pagination)


@admin_bp.route("/lookup/<string:kind>", methods=["GET", "POST"])
@login_required
@admin_required
def lookup_list(kind):
    model = LOOKUP_MODELS.get(kind)
    if not model:
        return render_template("errors/404.html"), 404

    form = LookupForm()
    if form.validate_on_submit():
        value = form.name.data.strip()
        if value and not model.query.filter_by(name=value).first():
            db.session.add(model(name=value))
            db.session.commit()
            flash("Запись добавлена.", "success")
        else:
            flash("Запись уже существует.", "warning")
        return redirect(url_for("admin.lookup_list", kind=kind))

    records = model.query.order_by(model.name).all()
    return render_template("admin/lookup_list.html", kind=kind, records=records, form=form)


@admin_bp.route("/lookup/<string:kind>/<int:record_id>/delete", methods=["POST"])
@login_required
@admin_required
def lookup_delete(kind, record_id):
    model = LOOKUP_MODELS.get(kind)
    if not model:
        return render_template("errors/404.html"), 404
    record = _get_or_404(model, record_id)
    db.session.delete(record)
    db.session.commit()
    flash("Запись удалена.", "info")
    return redirect(url_for("admin.lookup_list", kind=kind))
