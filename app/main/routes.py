from urllib.parse import urlencode

from flask import Blueprint, current_app, render_template, request
from flask_login import current_user

from ..models import Artist, Manufacturer, PaintingStyle, Shape, User
from ..services.item_service import build_catalog_query

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    latest_items = build_catalog_query(current_user, request.args).limit(6).all()
    return render_template("main/home.html", latest_items=latest_items)


@main_bp.route("/catalog")
def catalog():
    page = request.args.get("page", 1, type=int)
    query = build_catalog_query(current_user, request.args)
    pagination = query.paginate(page=page, per_page=current_app.config["ITEMS_PER_PAGE"], error_out=False)
    query_params = request.args.to_dict(flat=True)
    query_params.pop("page", None)
    pagination_query = urlencode(query_params)

    filters = {
        "manufacturers": Manufacturer.query.order_by(Manufacturer.name).all(),
        "artists": Artist.query.order_by(Artist.name).all(),
        "shapes": Shape.query.order_by(Shape.name).all(),
        "painting_styles": PaintingStyle.query.order_by(PaintingStyle.name).all(),
        "owners": User.query.order_by(User.username).all(),
    }
    return render_template("main/catalog.html", pagination=pagination, filters=filters, pagination_query=pagination_query)
