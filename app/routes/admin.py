from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import role_required, nocache

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
@nocache
def dashboard():
    return render_template("admin/dashboard.html")

@admin_bp.route("/siswa")
@login_required
@role_required("admin")
@nocache
def data_siswa():
    return render_template("admin/data_siswa.html")

@admin_bp.route("/modul")
@login_required
@role_required("admin")
@nocache
def modul_misi():
    return render_template("admin/modul_misi.html")

@admin_bp.route("/laporan")
@login_required
@role_required("admin")
@nocache
def nilai_laporan():
    return render_template("admin/nilai_laporan.html")

@admin_bp.route("/pengaturan")
@login_required
@role_required("admin")
@nocache
def pengaturan():
    return render_template("admin/pengaturan.html")
