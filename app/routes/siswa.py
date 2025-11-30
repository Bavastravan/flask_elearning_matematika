from flask import Blueprint, render_template, redirect, url_for
from app.utils.decorators import role_required  # di dalamnya biasanya sudah cek login

siswa_bp = Blueprint("siswa", __name__)

# Root siswa -> selalu arahkan ke dashboard
@siswa_bp.route("/")
@role_required("siswa")
def siswa_root():
    return redirect(url_for("siswa.dashboard"))

@siswa_bp.route("/dashboard")
@role_required("siswa")
def dashboard():
    return render_template("siswa/dashboard.html")

@siswa_bp.route("/buku")
@role_required("siswa")
def buku():
    return render_template("siswa/buku.html")

@siswa_bp.route("/misi")
@role_required("siswa")
def misi():
    return render_template("siswa/misi.html")

@siswa_bp.route("/progress")
@role_required("siswa")
def progress():
    return render_template("siswa/progress.html")
