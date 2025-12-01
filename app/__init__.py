from flask import Flask, redirect, url_for, flash
from .config import Config
from .extensions import db, login_manager, migrate
from .routes.main import main_bp
from .routes.auth import auth_bp
from .routes.siswa import siswa_bp
from .routes.admin import admin_bp
from .models import User
from .utils.seed_admin import create_default_admin


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Konfigurasi login manager
    login_manager.login_view = "auth.login"  # ← perbaiki dari "none" ke "auth.login"
    login_manager.login_message = None  # ← set None agar tidak double flash
    
    # Custom unauthorized handler untuk redirect tanpa parameter ?next=...
    @login_manager.unauthorized_handler
    def unauthorized():
        flash("Silakan login terlebih dahulu.", "warning")
        return redirect(url_for("auth.login"))  # redirect langsung tanpa parameter next

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(siswa_bp, url_prefix="/siswa")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Seed admin default setiap app start
    with app.app_context():
        create_default_admin()

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
