from flask import Flask
from .config import Config
from .extensions import db, login_manager, migrate
from .routes.main import main_bp
from .routes.auth import auth_bp
from .routes.siswa import siswa_bp
from .routes.admin import admin_bp
from .models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(siswa_bp, url_prefix="/siswa")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
