from flask import Blueprint, render_template
from app.utils.decorators import role_required

siswa_bp = Blueprint("siswa", __name__)

@siswa_bp.route("/dashboard")
@role_required("siswa")
def dashboard():
    return render_template("siswa/dashboard.html")
