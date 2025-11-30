from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.extensions import db
from app.models import User
from app.utils.security import hash_password, verify_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nama = request.form.get("nama")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("Email sudah terdaftar.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            nama=nama,
            email=email,
            password_hash=hash_password(password),
            role="siswa",
        )
        db.session.add(user)
        db.session.commit()

        flash("Registrasi berhasil, silakan login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not verify_password(user.password_hash, password):
            flash("Email atau password salah.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)
        # redirect berdasarkan role
        if user.role == "admin":
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("siswa.dashboard"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda telah logout.", "info")
    return redirect(url_for("main.index"))

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    # sementara: hanya tampilkan halaman kosong sederhana
    return render_template("auth/forgot_password.html")

