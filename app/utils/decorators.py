from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user, login_required

def role_required(role):
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
