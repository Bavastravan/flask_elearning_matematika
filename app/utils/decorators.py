from functools import wraps
from flask import redirect, url_for, flash, make_response
from flask_login import current_user, login_required


def nocache(view_func):
    """Decorator untuk mencegah browser cache halaman (untuk keamanan logout)."""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        resp = make_response(view_func(*args, **kwargs))
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
        return resp
    return wrapper


def role_required(role):
    """Decorator untuk validasi role user (siswa/admin)."""
    def wrapper(view_func):
        @wraps(view_func)
        @login_required
        def decorated_view(*args, **kwargs):
            if current_user.role != role:
                flash("Anda tidak punya akses ke halaman ini.", "danger")
                return redirect(url_for("main.index"))
            return view_func(*args, **kwargs)
        return decorated_view
    return wrapper
