from pathlib import Path

from flask import Flask, render_template

from .config import config_by_name
from .extensions import db, login_manager, migrate


def create_app(config_name: str = "development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .admin.routes import admin_bp
    from .auth.routes import auth_bp
    from .items.routes import items_bp
    from .main.routes import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(items_bp, url_prefix="/items")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.errorhandler(403)
    def forbidden(_):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal(_):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    return app
